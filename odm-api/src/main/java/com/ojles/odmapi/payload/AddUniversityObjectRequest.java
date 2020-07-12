package com.ojles.odmapi.payload;

import com.fasterxml.jackson.annotation.JsonTypeInfo;
import lombok.Getter;
import lombok.Setter;

import javax.sql.DataSource;

@Getter
@Setter
@JsonTypeInfo(
        use = JsonTypeInfo.Id.NAME,
        include = JsonTypeInfo.As.PROPERTY,
        property = "clazz"
)
public abstract class AddUniversityObjectRequest implements UniversityObjectRequest {
    private long id;
    private String name;
    private long majorId;

    public abstract UniversityObjectModel execute(DataSource dataSource);
}
