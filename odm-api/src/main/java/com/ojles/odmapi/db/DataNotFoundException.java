package com.ojles.odmapi.db;

public class DataNotFoundException extends DomainException {
    DataNotFoundException(String message) {
        super(message);
    }
}
