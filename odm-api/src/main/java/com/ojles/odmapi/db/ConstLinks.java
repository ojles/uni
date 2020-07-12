package com.ojles.odmapi.db;

import lombok.extern.slf4j.Slf4j;

import javax.sql.DataSource;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

@Slf4j
public class ConstLinks implements Links {
    private final DataSource dataSource;

    public ConstLinks(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    @Override
    public Link byId(long linkId) {
        String query = "select uo.name, uo.class, uo.major_id, l.url from university_object as uo inner join link as l on uo.id = l.id where uo.id = ?";
        try (Connection connection = dataSource.getConnection()) {
            try (PreparedStatement preparedStatement = connection.prepareStatement(query)) {
                preparedStatement.setLong(1, linkId);
                ResultSet resultSet = preparedStatement.executeQuery();
                if (!resultSet.next()) {
                    String errorMessage = "Link with id=" + linkId + " not found";
                    log.error(errorMessage);
                    throw new DataNotFoundException(errorMessage);
                }
                return new ConstLink(
                        new MyLink(
                                this.dataSource,
                                linkId
                        ),
                        resultSet.getString(1),
                        UniversityObjectClass.valueOf(resultSet.getString(2)),
                        resultSet.getLong(3),
                        resultSet.getString(4)
                );
            }
        } catch (SQLException e) {
            String errorMessage = "Failed to retrieve link with id=" + linkId;
            log.error(errorMessage, e);
            throw new DomainException(errorMessage, e);
        }
    }

    @Override
    public long insert(String name, UniversityObjectClass clazz, long majorId, String url) {
        throw new DomainException("You cannot insert link into const links");
    }
}
