package com.ojles.odmapi.db;

public interface Links {
    Link byId(long linkId);

    long insert(String name, UniversityObjectClass clazz, long majorId, String url);
}
