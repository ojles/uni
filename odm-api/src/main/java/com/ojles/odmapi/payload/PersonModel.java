package com.ojles.odmapi.payload;

import com.ojles.odmapi.db.Person;
import lombok.Getter;
import lombok.Setter;

import java.time.LocalDate;

@Getter
@Setter
public class PersonModel extends UniversityObjectModel {
    private LocalDate birthDate;

    public PersonModel(Person person) {
        super(person);
        this.birthDate = person.birthDate();
    }
}
