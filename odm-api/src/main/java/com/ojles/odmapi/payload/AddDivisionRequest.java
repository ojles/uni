package com.ojles.odmapi.payload;

import com.ojles.odmapi.db.*;
import lombok.Getter;
import lombok.Setter;

import javax.sql.DataSource;

@Getter
@Setter
public class AddDivisionRequest extends AddDepartmentRequest {
    private String roomNumber;

    @Override
    public DivisionModel execute(DataSource dataSource) {
        Divisions divisions = new MyDivisions(dataSource);
        long generatedId = divisions.insert(
                getName(),
                UniversityObjectClass.DIVISION,
                getMajorId(),
                getHeadOfId(),
                getEmail(),
                roomNumber

        );
        divisions = new ConstDivisions(dataSource);
        Division division = divisions.byId(generatedId);
        return new DivisionModel(division);
    }

    @Override
    public UniversityObjectClass clazz() {
        return UniversityObjectClass.DIVISION;
    }
}
