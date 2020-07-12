package com.ojles.odmapi.configuration;

import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.databind.jsontype.NamedType;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import com.ojles.odmapi.payload.UniversityObjectRequest;
import lombok.extern.slf4j.Slf4j;
import org.reflections.Reflections;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.lang.reflect.Modifier;

@Slf4j
@Configuration
public class ObjectMapperConfiguration {
    @Bean
    public ObjectMapper objectMapper() {
        ObjectMapper mapper = new ObjectMapper();
        registerUniversityObjectRequestSubtype(mapper);
        mapper.registerModule(new JavaTimeModule());
        mapper.disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);
        mapper.disable(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES);
        return mapper;
    }

    private void registerUniversityObjectRequestSubtype(ObjectMapper mapper) {
        try {
            Reflections reflections = new Reflections(UniversityObjectRequest.class.getPackage().getName());
            for (Class<? extends UniversityObjectRequest> requestSubclass : reflections.getSubTypesOf(UniversityObjectRequest.class)) {
                if (!Modifier.isAbstract(requestSubclass.getModifiers())) {
                    UniversityObjectRequest requestObject = requestSubclass.getConstructor().newInstance();
                    mapper.registerSubtypes(new NamedType(requestSubclass, requestObject.clazz().name()));
                }
            }
        } catch (ReflectiveOperationException e) {
            String message = "Failed to register " + UniversityObjectRequest.class.getCanonicalName() + " subtypes";
            log.error(message, e);
            throw new ConfigurationException(message, e);
        }
    }
}
