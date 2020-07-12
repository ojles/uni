package com.ojles.odmapi.db;

import java.time.LocalDate;

public interface Department extends UniversityObject {
    long headOfId();

    String email();

    LocalDate creationDate();

    void update(String name, long headOfId, String email);
}
