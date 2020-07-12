package com.ojles.odmapi.db;

public interface Division extends Department {
    String roomNumber();

    void update(String name, long headOfId, String email, String roomNumber);
}
