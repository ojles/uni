package com.ojles.odmapi.payload;

import com.ojles.odmapi.db.*;
import lombok.Getter;
import lombok.Setter;

import javax.sql.DataSource;
import java.time.LocalDate;

@Getter
@Setter
public class UpdatePersonRequest extends UpdateUniversityObjectRequest {
    private LocalDate birthDate;

    @Override
    public PersonModel execute(DataSource dataSource) {
        Person person = new MyPerson(dataSource, getId());
        person.update(getName(), birthDate);
        Persons persons = new ConstPersons(dataSource);
        person = persons.byId(getId());
        return new PersonModel(person);
    }

    @Override
    public UniversityObjectClass clazz() {
        return UniversityObjectClass.PERSON;
    }
}
