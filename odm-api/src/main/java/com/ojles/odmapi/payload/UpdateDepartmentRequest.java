package com.ojles.odmapi.payload;

import com.ojles.odmapi.db.*;
import lombok.Getter;
import lombok.Setter;

import javax.sql.DataSource;

@Getter
@Setter
public class UpdateDepartmentRequest extends UpdateUniversityObjectRequest {
    private long headOfId;
    private String email;

    @Override
    public DepartmentModel execute(DataSource dataSource) {
        Department department = new MyDepartment(dataSource, getId());
        department.update(getName(), headOfId, email);
        Departments departments = new ConstDepartments(dataSource);
        department = departments.byId(getId());
        return new DepartmentModel(department);
    }

    @Override
    public UniversityObjectClass clazz() {
        return UniversityObjectClass.DEPARTMENT;
    }
}
