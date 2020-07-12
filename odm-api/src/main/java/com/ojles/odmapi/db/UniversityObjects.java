package com.ojles.odmapi.db;

import java.util.List;

public interface UniversityObjects {
    List<UniversityObject> roots();

    List<UniversityObject> childrenOf(long majorId);

    UniversityObject byId(long objectId);

    long insert(String name, UniversityObjectClass clazz, long majorId);

    void deleteById(long objectId);
}
