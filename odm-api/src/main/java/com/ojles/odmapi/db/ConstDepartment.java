package com.ojles.odmapi.db;

import lombok.extern.slf4j.Slf4j;

import java.time.LocalDate;

@Slf4j
public class ConstDepartment extends ConstUniversityObject implements Department {
    private final long headOfId;
    private final String email;
    private final LocalDate creationDate;

    public ConstDepartment(UniversityObject origin,
                           String name,
                           UniversityObjectClass clazz,
                           long majorId,
                           long headOfId,
                           String email,
                           LocalDate creationDate) {
        super(origin, name, clazz, majorId);
        this.headOfId = headOfId;
        this.email = email;
        this.creationDate = creationDate;
    }

    @Override
    public long headOfId() {
        return headOfId;
    }

    @Override
    public String email() {
        return email;
    }

    @Override
    public LocalDate creationDate() {
        return creationDate;
    }

    @Override
    public void update(String name, long headOfId, String email) {
        throw new DomainException("You cannot update a const object");
    }
}
