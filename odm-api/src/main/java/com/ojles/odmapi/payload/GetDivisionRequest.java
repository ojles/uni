package com.ojles.odmapi.payload;

import com.ojles.odmapi.db.ConstDivisions;
import com.ojles.odmapi.db.Division;
import com.ojles.odmapi.db.Divisions;
import com.ojles.odmapi.db.UniversityObjectClass;

public class GetDivisionRequest extends GetDepartmentRequest {
    @Override
    public UniversityObjectModel execute() {
        Divisions divisions = new ConstDivisions(dataSource);
        Division division = divisions.byId(objectId);
        return new DivisionModel(division);
    }

    @Override
    public UniversityObjectClass clazz() {
        return UniversityObjectClass.DIVISION;
    }
}
