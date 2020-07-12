package com.ojles.odmapi.db;

import lombok.extern.slf4j.Slf4j;

import java.time.LocalDate;

@Slf4j
public class ConstDivision extends ConstDepartment implements Division {
    private final String roomNumber;

    public ConstDivision(UniversityObject origin,
                         String name,
                         UniversityObjectClass clazz,
                         long majorId,
                         long headOfId,
                         String email,
                         LocalDate creationDate,
                         String roomNumber) {
        super(origin, name, clazz, majorId, headOfId, email, creationDate);
        this.roomNumber = roomNumber;
    }

    @Override
    public String roomNumber() {
        return roomNumber;
    }

    @Override
    public void update(String name, long headOfId, String email, String roomNumber) {
        throw new DomainException("You cannot update a const object");
    }
}
