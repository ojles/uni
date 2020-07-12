package com.ojles.odmapi.db;

import lombok.extern.slf4j.Slf4j;

import javax.sql.DataSource;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

@Slf4j
public final class ConstDivisions implements Divisions {
    private final DataSource dataSource;

    public ConstDivisions(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    @Override
    public Division byId(long divisionId) {
        String query = "select uo.name, uo.class, uo.major_id, d.head_of_id, d.email, d.creation_date, dv.room_number from university_object as uo inner join department as d on uo.id = d.id inner join division as dv on d.id = dv.id where uo.id = ?";
        try (Connection connection = dataSource.getConnection()) {
            try (PreparedStatement preparedStatement = connection.prepareStatement(query)) {
                preparedStatement.setLong(1, divisionId);
                ResultSet resultSet = preparedStatement.executeQuery();
                if (!resultSet.next()) {
                    String errorMessage = "Division with id=" + divisionId + " not found";
                    log.error(errorMessage);
                    throw new DataNotFoundException(errorMessage);
                }
                return new ConstDivision(
                        new MyDivision(
                                this.dataSource,
                                divisionId
                        ),
                        resultSet.getString(1),
                        UniversityObjectClass.valueOf(resultSet.getString(2)),
                        resultSet.getLong(3),
                        resultSet.getLong(4),
                        resultSet.getString(5),
                        resultSet.getDate(6).toLocalDate(),
                        resultSet.getString(7)
                );
            }
        } catch (SQLException e) {
            String errorMessage = "Failed to retrieve division with id=" + divisionId;
            log.error(errorMessage, e);
            throw new DomainException(errorMessage, e);
        }
    }

    @Override
    public long insert(String name, UniversityObjectClass clazz, long majorId, long headOfId, String email, String roomNumber) {
        throw new DomainException("You cannot insert division into const division");
    }
}
