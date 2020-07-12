package com.ojles.odmapi.db;

import lombok.extern.slf4j.Slf4j;

import javax.sql.DataSource;
import java.sql.*;
import java.time.LocalDate;

@Slf4j
public class MyPersons implements Persons {
    private final DataSource dataSource;
    private final MyUniversityObjects universityObjects;

    public MyPersons(DataSource dataSource) {
        this.universityObjects = new MyUniversityObjects(dataSource);
        this.dataSource = dataSource;
    }

    @Override
    public Person byId(long personId) {
        return new MyPerson(this.dataSource, personId);
    }

    @Override
    public long insert(String name, UniversityObjectClass clazz, long majorId, LocalDate birthDate) {
        Long personId = universityObjects.insert(name, clazz, majorId);
        String query = "insert into person (id, birth_date) values (?, ?)";
        try (Connection connection = dataSource.getConnection()) {
            try (PreparedStatement preparedStatement = connection.prepareStatement(query, Statement.RETURN_GENERATED_KEYS)) {
                preparedStatement.setLong(1, personId);
                preparedStatement.setDate(2, Date.valueOf(birthDate));
                preparedStatement.executeUpdate();
                return personId;
            }
        } catch (SQLException e) {
            log.error("Failed to insert new person", e);
            throw new DomainException("Failed to insert new person", e);
        }
    }
}
