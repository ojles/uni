package com.ojles.odmapi.db;

import lombok.extern.slf4j.Slf4j;

import java.time.LocalDate;

@Slf4j
public class ConstFaculty extends ConstDepartment implements Faculty {
    private final String address;

    public ConstFaculty(UniversityObject origin,
                        String name,
                        UniversityObjectClass clazz,
                        long majorId,
                        long headOfId,
                        String email,
                        LocalDate creationDate,
                        String address) {
        super(origin, name, clazz, majorId, headOfId, email, creationDate);
        this.address = address;
    }

    @Override
    public String address() {
        return address;
    }

    @Override
    public void update(String name, long headOfId, String email, String address) {
        throw new DomainException("You cannot update a const object");
    }
}
