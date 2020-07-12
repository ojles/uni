package com.ojles.odmapi.db;

import lombok.extern.slf4j.Slf4j;

@Slf4j
public class ConstLink extends ConstUniversityObject implements Link {
    private String url;

    public ConstLink(UniversityObject origin,
                     String name,
                     UniversityObjectClass clazz,
                     long majorId,
                     String url) {
        super(origin, name, clazz, majorId);
        this.url = url;
    }

    @Override
    public String url() {
        return url;
    }

    @Override
    public void update(String name, String url) {
        throw new DomainException("You cannot update a const object");
    }
}
