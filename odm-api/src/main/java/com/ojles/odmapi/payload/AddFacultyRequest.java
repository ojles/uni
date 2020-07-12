package com.ojles.odmapi.payload;

import com.ojles.odmapi.db.*;
import lombok.Getter;
import lombok.Setter;

import javax.sql.DataSource;

@Getter
@Setter
public class AddFacultyRequest extends AddDepartmentRequest {
    private String address;

    @Override
    public FacultyModel execute(DataSource dataSource) {
        Faculties faculties = new MyFaculties(dataSource);
        long generatedId = faculties.insert(
                getName(),
                UniversityObjectClass.FACULTY,
                getMajorId(),
                getHeadOfId(),
                getEmail(),
                address
        );
        faculties = new ConstFaculties(dataSource);
        Faculty faculty = faculties.byId(generatedId);
        return new FacultyModel(faculty);
    }

    @Override
    public UniversityObjectClass clazz() {
        return UniversityObjectClass.FACULTY;
    }
}
