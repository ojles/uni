package com.ojles.odmapi.payload;

public class ObjectRequestException extends RuntimeException {
    ObjectRequestException(String message, Throwable cause) {
        super(message, cause);
    }
}
