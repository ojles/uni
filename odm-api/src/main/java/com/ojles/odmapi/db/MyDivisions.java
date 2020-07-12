package com.ojles.odmapi.db;

import lombok.extern.slf4j.Slf4j;

import javax.sql.DataSource;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.sql.Statement;

@Slf4j
public class MyDivisions implements Divisions {
    private final DataSource dataSource;
    private final MyDepartments departments;

    public MyDivisions(DataSource dataSource) {
        this.departments = new MyDepartments(dataSource);
        this.dataSource = dataSource;
    }

    @Override
    public Division byId(long divisionId) {
        return new MyDivision(this.dataSource, divisionId);
    }

    @Override
    public long insert(String name,
                       UniversityObjectClass clazz,
                       long majorId,
                       long headOfId,
                       String email,
                       String roomNumber) {
        Long divisionId = departments.insert(name, clazz, majorId, headOfId, email);
        String query = "insert into division (id, room_number) values (?, ?)";
        try (Connection connection = dataSource.getConnection()) {
            try (PreparedStatement preparedStatement = connection.prepareStatement(query, Statement.RETURN_GENERATED_KEYS)) {
                preparedStatement.setLong(1, divisionId);
                preparedStatement.setString(2, roomNumber);
                preparedStatement.executeUpdate();
                return divisionId;
            }
        } catch (SQLException e) {
            log.error("Failed to insert new division", e);
            throw new DomainException("Failed to insert new division", e);
        }
    }
}
