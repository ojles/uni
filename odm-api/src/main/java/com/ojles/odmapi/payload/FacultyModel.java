package com.ojles.odmapi.payload;

import com.ojles.odmapi.db.Faculty;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class FacultyModel extends DepartmentModel {
    private String address;

    public FacultyModel(Faculty faculty) {
        super(faculty);
        this.address = faculty.address();
    }
}
