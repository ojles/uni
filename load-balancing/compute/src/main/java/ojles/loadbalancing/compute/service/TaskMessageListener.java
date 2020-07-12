package ojles.loadbalancing.compute.service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import ojles.loadbalancing.compute.payload.TaskDto;
import org.springframework.stereotype.Component;

@Slf4j
@Component
@RequiredArgsConstructor
public class TaskMessageListener {
    private static final int STEP_INTERVAL_SECONDS = 4;

    private final TaskService taskService;

    public void receiveMessage(long taskId) throws InterruptedException {
        TaskDto task = taskService.takeToProccess(taskId);
        int steps = task.getExecutionSeconds() / STEP_INTERVAL_SECONDS;
        for (int step = 0; step < steps; step++) {
            Thread.sleep(STEP_INTERVAL_SECONDS * 1000);
            taskService.incrementProgress(task.getId(), STEP_INTERVAL_SECONDS);
        }
        Thread.sleep((task.getExecutionSeconds() % STEP_INTERVAL_SECONDS) * 1000);
        taskService.incrementProgress(task.getId(), task.getExecutionSeconds() % STEP_INTERVAL_SECONDS);
    }
}
