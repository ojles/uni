package com.ojles.odmapi.payload;

import com.ojles.odmapi.db.*;
import lombok.Getter;
import lombok.Setter;

import javax.sql.DataSource;
import java.time.LocalDate;

@Getter
@Setter
public class AddPersonRequest extends AddUniversityObjectRequest {
    private LocalDate birthDate;

    @Override
    public PersonModel execute(DataSource dataSource) {
        Persons persons = new MyPersons(dataSource);
        long generatedId = persons.insert(
                getName(),
                UniversityObjectClass.PERSON,
                getMajorId(),
                birthDate
        );
        persons = new ConstPersons(dataSource);
        Person person = persons.byId(generatedId);
        return new PersonModel(person);
    }

    @Override
    public UniversityObjectClass clazz() {
        return UniversityObjectClass.PERSON;
    }
}
