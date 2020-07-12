package com.ojles.odmapi.db;

import lombok.extern.slf4j.Slf4j;

import javax.sql.DataSource;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;

@Slf4j
public final class ConstUniversityObjects implements UniversityObjects {
    private final DataSource dataSource;

    public ConstUniversityObjects(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    @Override
    public List<UniversityObject> roots() {
        String query = "select id, name, class, major_id from university_object where major_id is null";
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
        String query = "select id, name, class, major_id from university_object where major_id = ?";
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
        String query = "select name, class, major_id from university_object where id = ?";
        try (Connection connection = dataSource.getConnection()) {
            try (PreparedStatement preparedStatement = connection.prepareStatement(query)) {
                preparedStatement.setLong(1, objectId);
                ResultSet resultSet = preparedStatement.executeQuery();
                if (!resultSet.next()) {
                    String errorMessage = "University object with id=" + objectId + " not found";
                    log.error(errorMessage);
                    throw new DataNotFoundException(errorMessage);
                }
                return new ConstUniversityObject(
                        new MyUniversityObject(
                                this.dataSource,
                                objectId
                        ),
                        resultSet.getString(1),
                        UniversityObjectClass.valueOf(resultSet.getString(2)),
                        resultSet.getLong(3)
                );
            }
        } catch (SQLException e) {
            String errorMessage = "Failed to retrieve university object with id=" + objectId;
            log.error(errorMessage, e);
            throw new DomainException(errorMessage, e);
        }
    }

    @Override
    public long insert(String name, UniversityObjectClass clazz, long majorId) {
        throw new DomainException("You cannot insert objects into const university objects");
    }

    @Override
    public void deleteById(long objectId) {
        throw new DomainException("You cannot delete const objects");
    }


    private ArrayList<UniversityObject> resultSetToList(ResultSet resultSet) throws SQLException {
        ArrayList<UniversityObject> universityObjects = new ArrayList<>();
        while (resultSet.next()) {
            universityObjects.add(
                    new ConstUniversityObject(
                            new MyUniversityObject(
                                    this.dataSource,
                                    resultSet.getLong(1)
                            ),
                            resultSet.getString(2),
                            UniversityObjectClass.valueOf(resultSet.getString(3)),
                            resultSet.getLong(4)
                    )
            );
        }
        return universityObjects;
    }
}
