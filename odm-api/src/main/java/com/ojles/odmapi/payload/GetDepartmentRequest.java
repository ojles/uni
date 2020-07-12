package com.ojles.odmapi.payload;

import com.ojles.odmapi.db.ConstDepartments;
import com.ojles.odmapi.db.Department;
import com.ojles.odmapi.db.Departments;
import com.ojles.odmapi.db.UniversityObjectClass;

public class GetDepartmentRequest extends GetUniversityObjectRequest {
    @Override
    public UniversityObjectModel execute() {
        Departments departments = new ConstDepartments(dataSource);
        Department department = departments.byId(objectId);
        return new DepartmentModel(department);
    }

    @Override
    public UniversityObjectClass clazz() {
        return UniversityObjectClass.DEPARTMENT;
    }
}
