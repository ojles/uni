package com.ojles.odmapi.payload;

import com.ojles.odmapi.db.*;
import lombok.Getter;
import lombok.Setter;

import javax.sql.DataSource;

@Getter
@Setter
public class UpdateDivisionRequest extends UpdateDepartmentRequest {
    private String roomNumber;

    @Override
    public DivisionModel execute(DataSource dataSource) {
        Division division = new MyDivision(dataSource, getId());
        division.update(getName(), getHeadOfId(), getEmail(), roomNumber);
        Divisions divisions = new ConstDivisions(dataSource);
        division = divisions.byId(getId());
        return new DivisionModel(division);
    }

    @Override
    public UniversityObjectClass clazz() {
        return UniversityObjectClass.DIVISION;
    }
}
