package ojles.loadbalancing.compute.service;

import lombok.RequiredArgsConstructor;
import ojles.loadbalancing.compute.model.Task;
import ojles.loadbalancing.compute.model.User;
import ojles.loadbalancing.compute.payload.TaskDto;
import ojles.loadbalancing.compute.repository.TaskRepository;
import ojles.loadbalancing.compute.repository.UserRepository;
import ojles.loadbalancing.compute.security.UserPrincipal;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class TaskService {
    private final TaskRepository taskRepository;
    private final RabbitTemplate rabbitTemplate;
    private final UserRepository userRepository;

    @Value("${app.instance-name}")
    private String instanceName;

    @Transactional
    public Task create(int executionSeconds) {
        Task task = new Task();
        task.setExecutionSeconds(executionSeconds);
        task.setInstanceName("unknown");
        task.setOwner(retrieveAuthorizedUser());
        task = taskRepository.save(task);
        rabbitTemplate.convertAndSend("tasks", task.getId());
        return task;
    }

    @Transactional
    public Task getOne(long id) {
        return taskRepository.getOne(id);
    }

    @Transactional
    public void incrementProgress(long taskId, int time) {
        Task task = taskRepository.getOne(taskId);
        task.setProgress(task.getProgress() + time);
        taskRepository.save(task);
    }

    @Transactional
    public TaskDto takeToProccess(long id) {
        Task task = taskRepository.getOne(id);
        task.setInstanceName(instanceName);
        task = taskRepository.save(task);
        return TaskDto.fromModel(task);
    }

    @Transactional
    public List<TaskDto> getAllForUser() {
        User owner = retrieveAuthorizedUser();
        return taskRepository.findAllByOwnerOrderByCreatedAt(owner)
                .stream()
                .map(TaskDto::fromModel)
                .collect(Collectors.toList());
    }

    @Transactional
    public List<TaskDto> getAll() {
        return taskRepository.findAll()
                .stream()
                .map(TaskDto::fromModel)
                .collect(Collectors.toList());
    }

    @Transactional
    public Task save(Task task) {
        return taskRepository.save(task);
    }

    private User retrieveAuthorizedUser() {
        UserPrincipal userPrincipal = (UserPrincipal) SecurityContextHolder.getContext()
                .getAuthentication()
                .getPrincipal();
        return userRepository.getOne(userPrincipal.getId());
    }
}
