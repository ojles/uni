package com.ojles.odmapi.db;

import java.time.LocalDate;

public interface Persons {
    Person byId(long personId);

    long insert(String name, UniversityObjectClass clazz, long majorId, LocalDate birthDate);
}
