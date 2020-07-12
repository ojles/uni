package com.ojles.odmapi.configuration;

import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;
import lombok.extern.slf4j.Slf4j;

import javax.sql.DataSource;
import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;


@Slf4j
public class DbConfiguration {
    private static final String DB_PROPERTIES_FILE_PATH = "hikari.properties";

    private static final DataSource dataSource;

    static {
        try (InputStream dbPropertiesStream = DbConfiguration.class
                .getClassLoader()
                .getResourceAsStream(DB_PROPERTIES_FILE_PATH)) {
            Properties dbProperties = new Properties();
            dbProperties.load(dbPropertiesStream);
            HikariConfig config = new HikariConfig(dbProperties);
            dataSource = new HikariDataSource(config);
        } catch (IOException e) {
            log.error("Failed to load database configuration", e);
            throw new ConfigurationException("Failed to load database configuration", e);
        }
    }

    public static DataSource getDataSource() {
        return dataSource;
    }
}
