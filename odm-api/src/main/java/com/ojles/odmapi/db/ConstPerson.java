package com.ojles.odmapi.db;

import lombok.extern.slf4j.Slf4j;

import java.time.LocalDate;

@Slf4j
public class ConstPerson extends ConstUniversityObject implements Person {
    private final LocalDate birthDate;

    public ConstPerson(UniversityObject origin, String name, UniversityObjectClass clazz, long majorId, LocalDate birthDate) {
        super(origin, name, clazz, majorId);
        this.birthDate = birthDate;
    }

    @Override
    public LocalDate birthDate() {
        return this.birthDate;
    }

    @Override
    public void update(String name, LocalDate birthDate) {
        throw new DomainException("You cannot update a const object");
    }
}
