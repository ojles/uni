package com.ojles.odmapi.payload;

import com.ojles.odmapi.db.ConstPersons;
import com.ojles.odmapi.db.Person;
import com.ojles.odmapi.db.Persons;
import com.ojles.odmapi.db.UniversityObjectClass;

public class GetPersonRequest extends GetUniversityObjectRequest {
    @Override
    public UniversityObjectModel execute() {
        Persons persons = new ConstPersons(dataSource);
        Person person = persons.byId(objectId);
        return new PersonModel(person);
    }

    @Override
    public UniversityObjectClass clazz() {
        return UniversityObjectClass.PERSON;
    }
}
