package com.ojles.odmapi.db;

public interface Faculty extends Department {
    String address();

    void update(String name, long headOfId, String email, String address);
}
