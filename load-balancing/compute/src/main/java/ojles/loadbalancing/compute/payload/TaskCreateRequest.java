package ojles.loadbalancing.compute.payload;

import lombok.Getter;
import lombok.Setter;
import org.hibernate.validator.constraints.Range;

@Getter
@Setter
public class TaskCreateRequest {
    @Range(min = 5, max = 60)
    private int executionSeconds;
}
