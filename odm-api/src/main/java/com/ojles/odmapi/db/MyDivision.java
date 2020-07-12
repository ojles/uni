package com.ojles.odmapi.db;

import lombok.extern.slf4j.Slf4j;

import javax.sql.DataSource;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;

@Slf4j
public class MyDivision extends MyDepartment implements Division {
    public MyDivision(DataSource dataSource, long id) {
        super(dataSource, id);
    }

    @Override
    public String roomNumber() {
        throw new MethodNotImplementedException("MyDivision#roomNumber() not implemented yet");
    }

    @Override
    public void update(String name, long headOfId, String email, String roomNumber) {
        super.update(name, headOfId, email);
        String query = "update division set room_number = ? where id = ?";
        try (Connection connection = dataSource.getConnection()) {
            try (PreparedStatement preparedStatement = connection.prepareStatement(query)) {
                preparedStatement.setString(1, roomNumber);
                preparedStatement.setLong(2, id());
                preparedStatement.executeUpdate();
            }
        } catch (SQLException e) {
            log.error("Failed to update division with id=" + id(), e);
            throw new DomainException("Failed to update division with id=" + id(), e);
        }
    }
}
