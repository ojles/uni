package com.ojles.odmapi.db;

public interface Departments {
    Department byId(long departmentId);

    long insert(String name, UniversityObjectClass clazz, long majorId, long headOfId, String email);
}
