package com.olespankiv;

import java.io.IOException;
import java.io.InputStream;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.util.Properties;

public class ActionLogger {
    enum Type {
        MOVE,
        RETURN;
    }

    private static final ActionLogger INSTANCE = new ActionLogger();
    private static final String DB_PROPERTIES_FILE_PATH = "db.properties";

    private Connection connection;

    public static ActionLogger getInstance() {
        return INSTANCE;
    }

    private ActionLogger() {
        try (InputStream dbPropertiesStream = ActionLogger.class
                .getClassLoader()
                .getResourceAsStream(DB_PROPERTIES_FILE_PATH)) {
            Properties dbProperties = new Properties();
            dbProperties.load(dbPropertiesStream);
            connection = DriverManager.getConnection(
                    dbProperties.getProperty("db.url"),
                    dbProperties.getProperty("db.username"),
                    dbProperties.getProperty("db.password")
            );
        } catch (IOException | SQLException e) {
            throw new RuntimeException("Failed to load database configuration", e);
        }
    }

    public void log(Type type, String source, String destination) {
        String query = "insert into action (type, source, destination) values (?, ?, ?)";
        try (PreparedStatement preparedStatement = connection.prepareStatement(query)) {
            preparedStatement.setString(1, type.name());
            preparedStatement.setString(2, source);
            preparedStatement.setString(3, destination);
            preparedStatement.executeUpdate();
        } catch (SQLException e) {
            throw new RuntimeException("Failed to log action", e);
        }
    }

    @Override
    protected void finalize() throws Throwable {
        super.finalize();
        connection.close();
    }
}
