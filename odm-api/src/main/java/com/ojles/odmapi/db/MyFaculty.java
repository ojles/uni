package com.ojles.odmapi.db;

import lombok.extern.slf4j.Slf4j;

import javax.sql.DataSource;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

@Slf4j
public class MyFaculty extends MyDepartment implements Faculty {
    public MyFaculty(DataSource dataSource, long id) {
        super(dataSource, id);
    }

    @Override
    public String address() {
        String query = "select address from faculty where id = ?";
        try (Connection connection = dataSource.getConnection()) {
            try (PreparedStatement preparedStatement = connection.prepareStatement(query)) {
                preparedStatement.setLong(1, id());
                ResultSet resultSet = preparedStatement.executeQuery();
                if (!resultSet.next()) {
                    throw new DataNotFoundException("Couldn't find address with id=" + id());
                }
                return resultSet.getString(1);
            }
        } catch (SQLException e) {
            log.error("Failed to retrieve address", e);
            throw new DomainException("Failed to retrieve address", e);
        }
    }

    @Override
    public void update(String name, long headOfId, String email, String address) {
        super.update(name, headOfId, email);
        String query = "update faculty set address = ? where id = ?";
        try (Connection connection = dataSource.getConnection()) {
            try (PreparedStatement preparedStatement = connection.prepareStatement(query)) {
                preparedStatement.setString(1, address);
                preparedStatement.setLong(2, id());
                preparedStatement.executeUpdate();
            }
        } catch (SQLException e) {
            log.error("Failed to update faculty with id=" + id(), e);
            throw new DomainException("Failed to update faculty with id=" + id(), e);
        }
    }
}
