package com.ojles.odmapi.db;

import lombok.extern.slf4j.Slf4j;

@Slf4j
public class ConstUniversityObject implements UniversityObject {
    private final UniversityObject origin;
    private final String name;
    private final UniversityObjectClass clazz;
    private final long majorId;

    public ConstUniversityObject(UniversityObject origin, String name, UniversityObjectClass clazz, long majorId) {
        this.origin = origin;
        this.name = name;
        this.clazz = clazz;
        this.majorId = majorId;
    }

    @Override
    public long id() {
        return origin.id();
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public UniversityObjectClass clazz() {
        return clazz;
    }

    @Override
    public long majorId() {
        return majorId;
    }

    @Override
    public void update(String name) {
        throw new DomainException("You cannot update a const object");
    }
}
