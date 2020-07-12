package com.ojles.odmapi.payload;

import com.ojles.odmapi.db.UniversityObject;
import com.ojles.odmapi.db.UniversityObjectClass;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
public class UniversityObjectModel {
    private long id;
    private String name;
    private UniversityObjectClass clazz;
    private long majorId;

    public UniversityObjectModel(UniversityObject object) {
        this.id = object.id();
        this.name = object.name();
        this.clazz = object.clazz();
        this.majorId = object.majorId();
    }
}
