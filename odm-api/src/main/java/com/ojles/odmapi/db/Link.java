package com.ojles.odmapi.db;

public interface Link extends UniversityObject {
    String url();

    void update(String name, String url);
}
