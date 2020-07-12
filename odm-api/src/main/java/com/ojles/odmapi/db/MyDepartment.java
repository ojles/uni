package com.ojles.odmapi.db;

import lombok.extern.slf4j.Slf4j;

import javax.sql.DataSource;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.time.LocalDate;

@Slf4j
public class MyDepartment extends MyUniversityObject implements Department {
    public MyDepartment(DataSource dataSource, long id) {
        super(dataSource, id);
    }

    @Override
    public long headOfId() {
        String query = "select head_of_id from department where id = ?";
        try (Connection connection = dataSource.getConnection()) {
            try (PreparedStatement preparedStatement = connection.prepareStatement(query)) {
                preparedStatement.setLong(1, id());
                ResultSet resultSet = preparedStatement.executeQuery();
                if (!resultSet.next()) {
                    throw new DataNotFoundException("Couldn't find headOfId with id=" + id());
                }
                return resultSet.getLong(1);
            }
        } catch (SQLException e) {
            log.error("Failed to retrieve headOfId", e);
            throw new DomainException("Failed to retrieve headOfId", e);
        }
    }

    @Override
    public String email() {
        String query = "select email from department where id = ?";
        try (Connection connection = dataSource.getConnection()) {
            try (PreparedStatement preparedStatement = connection.prepareStatement(query)) {
                preparedStatement.setLong(1, id());
                ResultSet resultSet = preparedStatement.executeQuery();
                if (!resultSet.next()) {
                    throw new DataNotFoundException("Couldn't find email with id=" + id());
                }
                return resultSet.getString(1);
            }
        } catch (SQLException e) {
            log.error("Failed to retrieve email", e);
            throw new DomainException("Failed to retrieve email", e);
        }
    }

    @Override
    public LocalDate creationDate() {
        String query = "select creation_date from department where id = ?";
        try (Connection connection = dataSource.getConnection()) {
            try (PreparedStatement preparedStatement = connection.prepareStatement(query)) {
                preparedStatement.setLong(1, id());
                ResultSet resultSet = preparedStatement.executeQuery();
                if (!resultSet.next()) {
                    throw new DataNotFoundException("Couldn't find creationDate with id=" + id());
                }
                return resultSet.getDate(1).toLocalDate();
            }
        } catch (SQLException e) {
            log.error("Failed to retrieve creationDate", e);
            throw new DomainException("Failed to retrieve creationDate", e);
        }
    }

    @Override
    public void update(String name, long headOfId, String email) {
        super.update(name);
        String query = "update department set head_of_id = ?, email = ? where id = ?";
        try (Connection connection = dataSource.getConnection()) {
            try (PreparedStatement preparedStatement = connection.prepareStatement(query)) {
                preparedStatement.setLong(1, headOfId);
                preparedStatement.setString(2, email);
                preparedStatement.setLong(3, id());
                preparedStatement.executeUpdate();
            }
        } catch (SQLException e) {
            log.error("Failed to update department with id=" + id(), e);
            throw new DomainException("Failed to update department with id=" + id(), e);
        }
    }
}
