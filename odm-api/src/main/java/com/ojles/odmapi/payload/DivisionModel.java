package com.ojles.odmapi.payload;

import com.ojles.odmapi.db.Division;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class DivisionModel extends DepartmentModel {
    private String roomNumber;

    public DivisionModel(Division division) {
        super(division);
        this.roomNumber = division.roomNumber();
    }
}
