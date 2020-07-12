package com.ojles.odmapi.payload;

import com.ojles.odmapi.db.Department;
import lombok.Getter;
import lombok.Setter;

import java.time.LocalDate;

@Getter
@Setter
public class DepartmentModel extends UniversityObjectModel {
    private long headOfId;
    private String email;
    private LocalDate creationDate;

    public DepartmentModel(Department department) {
        super(department);
        this.headOfId = department.headOfId();
        this.email = department.email();
        this.creationDate = department.creationDate();
    }
}
