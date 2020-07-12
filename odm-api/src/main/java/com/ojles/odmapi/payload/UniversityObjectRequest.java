package com.ojles.odmapi.payload;

import com.ojles.odmapi.db.UniversityObjectClass;

public interface UniversityObjectRequest {
    /**
     * Returns class that is handled by this request object.
     */
    UniversityObjectClass clazz();
}
