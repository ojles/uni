package com.ojles.odmapi.db;

import lombok.extern.slf4j.Slf4j;

import javax.sql.DataSource;
import java.sql.*;
import java.time.LocalDate;

@Slf4j
public class MyPerson extends MyUniversityObject implements Person {
    public MyPerson(DataSource dataSource, long id) {
        super(dataSource, id);
    }

    public LocalDate birthDate() {
        String query = "select birth_date from person where id = ?";
        try (Connection connection = dataSource.getConnection()) {
            try (PreparedStatement preparedStatement = connection.prepareStatement(query)) {
                preparedStatement.setLong(1, id());
                ResultSet resultSet = preparedStatement.executeQuery();
                if (!resultSet.next()) {
                    throw new DataNotFoundException("Couldn't find birth date with id=" + id());
                }
                return resultSet.getDate(1).toLocalDate();
            }
        } catch (SQLException e) {
            log.error("Failed to retrieve birth date", e);
            throw new DomainException("Failed to retrieve birth date", e);
        }
    }

    // TODO: share connection in same thread
    public void update(String name, LocalDate birthDate) {
        super.update(name);
        String query = "update person set birth_date = ? where id = ?";
        try (Connection connection = dataSource.getConnection()) {
            try (PreparedStatement preparedStatement = connection.prepareStatement(query)) {
                preparedStatement.setDate(1, Date.valueOf(birthDate));
                preparedStatement.setLong(2, id());
                preparedStatement.executeUpdate();
            }
        } catch (SQLException e) {
            log.error("Failed to update person with id=" + id(), e);
            throw new DomainException("Failed to update person with id=" + id(), e);
        }
    }
}
