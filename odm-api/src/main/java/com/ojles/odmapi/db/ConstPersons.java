package com.ojles.odmapi.db;

import lombok.extern.slf4j.Slf4j;

import javax.sql.DataSource;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.time.LocalDate;

@Slf4j
public final class ConstPersons implements Persons {
    private final DataSource dataSource;

    public ConstPersons(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    @Override
    public Person byId(long personId) {
        String query = "select ub.name, ub.class, ub.major_id, p.birth_date from university_object as ub inner join person as p on ub.id = p.id where ub.id = ?";
        try (Connection connection = dataSource.getConnection()) {
            try (PreparedStatement preparedStatement = connection.prepareStatement(query)) {
                preparedStatement.setLong(1, personId);
                ResultSet resultSet = preparedStatement.executeQuery();
                if (!resultSet.next()) {
                    String errorMessage = "Person with id=" + personId + " not found";
                    log.error(errorMessage);
                    throw new DataNotFoundException(errorMessage);
                }
                return new ConstPerson(
                        new MyPerson(
                                this.dataSource,
                                personId
                        ),
                        resultSet.getString(1),
                        UniversityObjectClass.valueOf(resultSet.getString(2)),
                        resultSet.getLong(3),
                        resultSet.getDate(4).toLocalDate()
                );
            }
        } catch (SQLException e) {
            String errorMessage = "Failed to retrieve person with id=" + personId;
            log.error(errorMessage, e);
            throw new DomainException(errorMessage, e);
        }
    }

    @Override
    public long insert(String name, UniversityObjectClass clazz, long majorId, LocalDate birthDate) {
        throw new DomainException("You cannot insert person into const persons");
    }
}
