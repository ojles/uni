package com.ojles.odmapi.db;

import lombok.extern.slf4j.Slf4j;

import javax.sql.DataSource;
import java.sql.*;
import java.util.Calendar;

@Slf4j
public class MyDepartments implements Departments {
    private final DataSource dataSource;
    private final MyUniversityObjects universityObjects;

    public MyDepartments(DataSource dataSource) {
        this.universityObjects = new MyUniversityObjects(dataSource);
        this.dataSource = dataSource;
    }

    @Override
    public Department byId(long departmentId) {
        return new MyDepartment(this.dataSource, departmentId);
    }

    @Override
    public long insert(String name,
                       UniversityObjectClass clazz,
                       long majorId,
                       long headOfId,
                       String email) {
        Long departmentId = universityObjects.insert(name, clazz, majorId);
        String query = "insert into department (id, head_of_id, email, creation_date) values (?, ?, ?, ?)";
        try (Connection connection = dataSource.getConnection()) {
            try (PreparedStatement preparedStatement = connection.prepareStatement(query, Statement.RETURN_GENERATED_KEYS)) {
                preparedStatement.setLong(1, departmentId);
                preparedStatement.setLong(2, headOfId);
                preparedStatement.setString(3, email);
                preparedStatement.setDate(4, new Date(Calendar.getInstance().getTime().getTime()));
                preparedStatement.executeUpdate();
                return departmentId;
            }
        } catch (SQLException e) {
            log.error("Failed to insert new department", e);
            throw new DomainException("Failed to insert new department", e);
        }
    }
}
