package com.ojles.odmapi.db;

public interface Faculties {
    Faculty byId(long facultyId);

    long insert(String name, UniversityObjectClass clazz, long majorId, long headOfId, String email, String address);
}
