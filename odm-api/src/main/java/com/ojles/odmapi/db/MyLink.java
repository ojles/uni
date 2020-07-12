package com.ojles.odmapi.db;

import lombok.extern.slf4j.Slf4j;

import javax.sql.DataSource;
import java.sql.*;

@Slf4j
public class MyLink extends MyUniversityObject implements Link {
    public MyLink(DataSource dataSource, long id) {
        super(dataSource, id);
    }

    @Override
    public String url() {
        String query = "select url from link where id = ?";
        try (Connection connection = dataSource.getConnection()) {
            try (PreparedStatement preparedStatement = connection.prepareStatement(query)) {
                preparedStatement.setLong(1, id());
                ResultSet resultSet = preparedStatement.executeQuery();
                if (!resultSet.next()) {
                    throw new DataNotFoundException("Couldn't find link with id=" + id());
                }
                return resultSet.getString(1);
            }
        } catch (SQLException e) {
            log.error("Failed to retrieve link", e);
            throw new DomainException("Failed to retrieve link", e);
        }
    }

    public void update(String name, String url) {
        super.update(name);
        String query = "update link set url = ? where id = ?";
        try (Connection connection = dataSource.getConnection()) {
            try (PreparedStatement preparedStatement = connection.prepareStatement(query)) {
                preparedStatement.setString(1, url);
                preparedStatement.setLong(2, id());
                preparedStatement.executeUpdate();
            }
        } catch (SQLException e) {
            log.error("Failed to update link with id=" + id(), e);
            throw new DomainException("Failed to update link with id=" + id(), e);
        }
    }
}
