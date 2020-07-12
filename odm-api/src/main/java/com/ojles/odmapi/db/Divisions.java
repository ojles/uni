package com.ojles.odmapi.db;

public interface Divisions {
    Division byId(long divisionId);

    long insert(String name, UniversityObjectClass clazz, long majorId, long headOfId, String email, String roomNumber);
}
