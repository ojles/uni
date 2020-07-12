package com.ojles.odmapi.payload;

import com.ojles.odmapi.db.*;
import lombok.Getter;
import lombok.Setter;

import javax.sql.DataSource;

@Getter
@Setter
public class AddDepartmentRequest extends AddUniversityObjectRequest {
    private long headOfId;
    private String email;

    @Override
    public DepartmentModel execute(DataSource dataSource) {
        Departments departments = new MyDepartments(dataSource);
        long generatedId = departments.insert(
                getName(),
                UniversityObjectClass.DEPARTMENT,
                getMajorId(),
                headOfId,
                email
        );
        departments = new ConstDepartments(dataSource);
        Department department = departments.byId(generatedId);
        return new DepartmentModel(department);
    }

    @Override
    public UniversityObjectClass clazz() {
        return UniversityObjectClass.DEPARTMENT;
    }
}
