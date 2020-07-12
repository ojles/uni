package ojles.loadbalancing.compute.payload;

import lombok.Getter;
import lombok.Setter;
import ojles.loadbalancing.compute.model.Task;

import java.time.LocalDateTime;

@Getter
@Setter
public class TaskDto {
    private long id;
    private long ownerId;
    private LocalDateTime createdAt;
    private int executionSeconds;
    private int progress;
    private String instanceName;

    public static TaskDto fromModel(Task task) {
        TaskDto dto = new TaskDto();
        dto.setId(task.getId());
        dto.setOwnerId(task.getOwner().getId());
        dto.setCreatedAt(task.getCreatedAt());
        dto.setExecutionSeconds(task.getExecutionSeconds());
        dto.setProgress(task.getProgress());
        dto.setInstanceName(task.getInstanceName());
        return dto;
    }
}
