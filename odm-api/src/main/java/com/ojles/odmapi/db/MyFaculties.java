package com.ojles.odmapi.db;

import lombok.extern.slf4j.Slf4j;

import javax.sql.DataSource;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.sql.Statement;

@Slf4j
public class MyFaculties implements Faculties {
    private final DataSource dataSource;
    private final MyDepartments departments;

    public MyFaculties(DataSource dataSource) {
        this.departments = new MyDepartments(dataSource);
        this.dataSource = dataSource;
    }

    @Override
    public Faculty byId(long facultyId) {
        return new MyFaculty(this.dataSource, facultyId);
    }

    @Override
    public long insert(String name,
                       UniversityObjectClass clazz,
                       long majorId,
                       long headOfId,
                       String email,
                       String address) {
        Long facultyId = departments.insert(name, clazz, majorId, headOfId, email);
        String query = "insert into faculty (id, address) values (?, ?)";
        try (Connection connection = dataSource.getConnection()) {
            try (PreparedStatement preparedStatement = connection.prepareStatement(query, Statement.RETURN_GENERATED_KEYS)) {
                preparedStatement.setLong(1, facultyId);
                preparedStatement.setString(2, address);
                preparedStatement.executeUpdate();
                return facultyId;
            }
        } catch (SQLException e) {
            log.error("Failed to insert new faculty", e);
            throw new DomainException("Failed to insert new faculty", e);
        }
    }
}
