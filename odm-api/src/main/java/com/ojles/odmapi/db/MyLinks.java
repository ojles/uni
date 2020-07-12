package com.ojles.odmapi.db;

import lombok.extern.slf4j.Slf4j;

import javax.sql.DataSource;
import java.sql.*;

@Slf4j
public class MyLinks implements Links {
    private final DataSource dataSource;
    private final MyUniversityObjects universityObjects;

    public MyLinks(DataSource dataSource) {
        this.universityObjects = new MyUniversityObjects(dataSource);
        this.dataSource = dataSource;
    }

    @Override
    public Link byId(long linkId) {
        return new MyLink(dataSource, linkId);
    }

    @Override
    public long insert(String name, UniversityObjectClass clazz, long majorId, String url) {
        Long linkId = universityObjects.insert(name, clazz, majorId);
        String query = "insert into link (id, url) values (?, ?)";
        try (Connection connection = dataSource.getConnection()) {
            try (PreparedStatement preparedStatement = connection.prepareStatement(query, Statement.RETURN_GENERATED_KEYS)) {
                preparedStatement.setLong(1, linkId);
                preparedStatement.setString(2, url);
                preparedStatement.executeUpdate();
                return linkId;
            }
        } catch (SQLException e) {
            log.error("Failed to insert new link", e);
            throw new DomainException("Failed to insert new link", e);
        }
    }
}
