package com.ojles.odmapi.db;

public interface UniversityObject {
    long id();

    String name();

    long majorId();

    UniversityObjectClass clazz();

    void update(String name);
}
