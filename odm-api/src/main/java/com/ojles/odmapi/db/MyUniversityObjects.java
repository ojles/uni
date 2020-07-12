package com.ojles.odmapi.db;

import lombok.extern.slf4j.Slf4j;

import javax.sql.DataSource;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;

@Slf4j
public class MyUniversityObjects implements UniversityObjects {
    private final DataSource dataSource;

    public MyUniversityObjects(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    @Override
    public List<UniversityObject> roots() {
        String query = "select id from university_object where major_id is null";
        try (Connection connection = dataSource.getConnection()) {
            try (Statement statement = connection.createStatement()) {
                ResultSet resultSet = statement.executeQuery(query);
                return resultSetToList(resultSet);
            }
        } catch (SQLException e) {
            log.error("Failed to retrieve root objects", e);
            throw new DomainException("Failed to retrieve root objects", e);
        }
    }

    @Override
    public List<UniversityObject> childrenOf(long majorId) {
        String query = "select id from university_object where major_id = ?";
        try (Connection connection = dataSource.getConnection()) {
            try (PreparedStatement preparedStatement = connection.prepareStatement(query)) {
                preparedStatement.setLong(1, majorId);
                ResultSet resultSet = preparedStatement.executeQuery();
                return resultSetToList(resultSet);
            }
        } catch (SQLException e) {
            String errorMessage = "Failed to retrieve children of majorId=" + majorId;
            log.error(errorMessage, e);
            throw new DomainException(errorMessage, e);
        }
    }

    @Override
    public UniversityObject byId(long objectId) {
        return new MyUniversityObject(this.dataSource, objectId);
    }

    @Override
    public long insert(String name, UniversityObjectClass clazz, long majorId) {
        String query = "insert into university_object (name, class, major_id) values (?, ?, ?)";
        try (Connection connection = dataSource.getConnection()) {
            try (PreparedStatement preparedStatement = connection.prepareStatement(query, Statement.RETURN_GENERATED_KEYS)) {
                preparedStatement.setString(1, name);
                preparedStatement.setString(2, clazz.name());
                preparedStatement.setLong(3, majorId);
                preparedStatement.executeUpdate();
                ResultSet generatedKeys = preparedStatement.getGeneratedKeys();
                if (generatedKeys.next()) {
                    return generatedKeys.getLong(1);
                } else {
                    String message = "Failed to insert university object with name=" + name + ", empty set of generated keys";
                    log.error(message);
                    throw new DomainException(message);
                }
            }
        } catch (SQLException e) {
            log.error("Failed to insert new university object", e);
            throw new DomainException("Failed to insert new university object", e);
        }
    }

    @Override
    public void deleteById(long objectId) {
        String query = "delete from university_object where id = ?";
        try (Connection connection = dataSource.getConnection()) {
            try (PreparedStatement preparedStatement = connection.prepareStatement(query)) {
                preparedStatement.setLong(1, objectId);
                preparedStatement.executeUpdate();
            }
        } catch (SQLException e) {
            log.error("Failed to delete university object with id=" + objectId, e);
            throw new DomainException("Failed to delete university object with id=" + objectId, e);
        }
    }

    private ArrayList<UniversityObject> resultSetToList(ResultSet resultSet) throws SQLException {
        ArrayList<UniversityObject> universityObjects = new ArrayList<>();
        while (resultSet.next()) {
            universityObjects.add(
                    new MyUniversityObject(
                            this.dataSource,
                            resultSet.getLong(1)
                    )
            );
        }
        return universityObjects;
    }
}
