package com.ojles.odmapi.payload;

import com.ojles.odmapi.db.ConstFaculties;
import com.ojles.odmapi.db.Faculties;
import com.ojles.odmapi.db.Faculty;
import com.ojles.odmapi.db.UniversityObjectClass;

public class GetFacultyRequest extends GetUniversityObjectRequest {
    @Override
    public UniversityObjectModel execute() {
        Faculties faculties = new ConstFaculties(dataSource);
        Faculty faculty = faculties.byId(objectId);
        return new FacultyModel(faculty);
    }

    @Override
    public UniversityObjectClass clazz() {
        return UniversityObjectClass.FACULTY;
    }
}
