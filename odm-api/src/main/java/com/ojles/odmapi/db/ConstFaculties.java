package com.ojles.odmapi.db;

import lombok.extern.slf4j.Slf4j;

import javax.sql.DataSource;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

@Slf4j
public final class ConstFaculties implements Faculties {
    private final DataSource dataSource;

    public ConstFaculties(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    @Override
    public Faculty byId(long facultyId) {
        String query = "select uo.name, uo.class, uo.major_id, d.head_of_id, d.email, d.creation_date, f.address from university_object as uo inner join department as d on uo.id = d.id inner join faculty as f on d.id = f.id where uo.id = ?";
        try (Connection connection = dataSource.getConnection()) {
            try (PreparedStatement preparedStatement = connection.prepareStatement(query)) {
                preparedStatement.setLong(1, facultyId);
                ResultSet resultSet = preparedStatement.executeQuery();
                if (!resultSet.next()) {
                    String errorMessage = "Faculty with id=" + facultyId + " not found";
                    log.error(errorMessage);
                    throw new DataNotFoundException(errorMessage);
                }
                return new ConstFaculty(
                        new MyFaculty(
                                this.dataSource,
                                facultyId
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
            String errorMessage = "Failed to retrieve faculty with id=" + facultyId;
            log.error(errorMessage, e);
            throw new DomainException(errorMessage, e);
        }
    }

    @Override
    public long insert(String name, UniversityObjectClass clazz, long majorId, long headOfId, String email, String address) {
        throw new DomainException("You cannot insert faculty into const faculty");
    }
}
