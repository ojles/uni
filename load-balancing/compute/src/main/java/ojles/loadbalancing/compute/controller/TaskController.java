package ojles.loadbalancing.compute.controller;

import lombok.RequiredArgsConstructor;
import ojles.loadbalancing.compute.payload.ApiResponse;
import ojles.loadbalancing.compute.payload.TaskCreateRequest;
import ojles.loadbalancing.compute.payload.TaskDto;
import ojles.loadbalancing.compute.service.TaskService;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import java.util.List;

@RestController
@RequiredArgsConstructor
@RequestMapping("/api/tasks")
public class TaskController {
    private final TaskService taskService;

    @GetMapping("")
    @PreAuthorize("hasRole('USER')")
    public List<TaskDto> getAll() {
        return taskService.getAllForUser();
    }

    @PostMapping("")
    @PreAuthorize("hasRole('USER')")
    public ApiResponse create(@Valid @RequestBody TaskCreateRequest request) {
        taskService.create(request.getExecutionSeconds());
        return new ApiResponse(true, "Created task");
    }
}
