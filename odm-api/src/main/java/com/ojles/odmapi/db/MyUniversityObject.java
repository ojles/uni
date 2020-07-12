package com.ojles.odmapi.db;

import lombok.extern.slf4j.Slf4j;

import javax.sql.DataSource;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

@Slf4j
public class MyUniversityObject implements UniversityObject {
    protected final DataSource dataSource;
    private final long id;

    public MyUniversityObject(DataSource dataSource, long id) {
        this.dataSource = dataSource;
        this.id = id;
    }

    @Override
    public long id() {
        return id;
    }

    @Override
    public String name() {
        String query = "select name from university_object where id = ?";
        try (Connection connection = dataSource.getConnection()) {
            try (PreparedStatement preparedStatement = connection.prepareStatement(query)) {
                preparedStatement.setLong(1, id);
                ResultSet resultSet = preparedStatement.executeQuery();
                if (!resultSet.next()) {
                    throw new DataNotFoundException("Couldn't find name with id=" + id);
                }
                return resultSet.getString(1);
            }
        } catch (SQLException e) {
            log.error("Failed to retrieve name", e);
            throw new DomainException("Failed to retrieve name", e);
        }
    }

    @Override
    public long majorId() {
        String query = "select major_id from university_object where id = ?";
        try (Connection connection = dataSource.getConnection()) {
            try (PreparedStatement preparedStatement = connection.prepareStatement(query)) {
                preparedStatement.setLong(1, id);
                ResultSet resultSet = preparedStatement.executeQuery();
                if (!resultSet.next()) {
                    throw new DataNotFoundException("Couldn't find majorId with id=" + id);
                }
                return resultSet.getLong(1);
            }
        } catch (SQLException e) {
            log.error("Failed to retrieve majorId", e);
            throw new DomainException("Failed to retrieve majorId", e);
        }
    }

    @Override
    public UniversityObjectClass clazz() {
        String query = "select class from university_object where id = ?";
        try (Connection connection = dataSource.getConnection()) {
            try (PreparedStatement preparedStatement = connection.prepareStatement(query)) {
                preparedStatement.setLong(1, id);
                ResultSet resultSet = preparedStatement.executeQuery();
                if (!resultSet.next()) {
                    throw new DataNotFoundException("Couldn't find object class with id=" + id);
                }
                return UniversityObjectClass.valueOf(resultSet.getString(1));
            }
        } catch (SQLException e) {
            log.error("Failed to retrieve object class", e);
            throw new DomainException("Failed to retrieve object class", e);
        }
    }

    @Override
    public void update(String name) {
        String query = "update university_object set name = ? where id = ?";
        try (Connection connection = dataSource.getConnection()) {
            try (PreparedStatement preparedStatement = connection.prepareStatement(query)) {
                preparedStatement.setString(1, name);
                preparedStatement.setLong(2, id);
                preparedStatement.executeUpdate();
            }
        } catch (SQLException e) {
            log.error("Failed to update university object with id=" + id, e);
            throw new DomainException("Failed to update university object with id=" + id, e);
        }
    }
}
