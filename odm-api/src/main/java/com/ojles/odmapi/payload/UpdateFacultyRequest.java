package com.ojles.odmapi.payload;

import com.ojles.odmapi.db.*;
import lombok.Getter;
import lombok.Setter;

import javax.sql.DataSource;

@Getter
@Setter
public class UpdateFacultyRequest extends UpdateDepartmentRequest {
    private String address;

    @Override
    public FacultyModel execute(DataSource dataSource) {
        Faculty faculty = new MyFaculty(dataSource, getId());
        faculty.update(getName(), getHeadOfId(), getEmail(), address);
        Faculties faculties = new ConstFaculties(dataSource);
        faculty = faculties.byId(getId());
        return new FacultyModel(faculty);
    }

    @Override
    public UniversityObjectClass clazz() {
        return UniversityObjectClass.FACULTY;
    }
}
