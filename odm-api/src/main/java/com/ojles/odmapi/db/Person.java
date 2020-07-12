package com.ojles.odmapi.db;

import java.time.LocalDate;

public interface Person extends UniversityObject {
    LocalDate birthDate();

    void update(String name, LocalDate birthDate);
}
