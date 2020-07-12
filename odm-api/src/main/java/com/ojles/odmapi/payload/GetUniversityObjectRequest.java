package com.ojles.odmapi.payload;

import com.ojles.odmapi.db.MyUniversityObject;
import com.ojles.odmapi.db.UniversityObject;
import com.ojles.odmapi.db.UniversityObjectClass;
import lombok.Getter;
import lombok.extern.slf4j.Slf4j;
import org.reflections.Reflections;

import javax.sql.DataSource;
import java.lang.reflect.Modifier;
import java.util.HashMap;
import java.util.Map;

@Slf4j
@Getter
public abstract class GetUniversityObjectRequest implements UniversityObjectRequest {
    private static Map<UniversityObjectClass, Class<? extends GetUniversityObjectRequest>> REQUEST_SUBCLASSES;

    protected DataSource dataSource;
    protected long objectId;

    static {
        REQUEST_SUBCLASSES = new HashMap<>();
        Reflections reflections = new Reflections(GetUniversityObjectRequest.class.getPackage().getName());
        try {
            for (Class<? extends GetUniversityObjectRequest> requestSubclass
                    : reflections.getSubTypesOf(GetUniversityObjectRequest.class)) {
                if (!Modifier.isAbstract(requestSubclass.getModifiers())) {
                    GetUniversityObjectRequest requestObject = requestSubclass.getConstructor().newInstance();
                    REQUEST_SUBCLASSES.put(requestObject.clazz(), requestSubclass);
                }
            }
        } catch (ReflectiveOperationException e) {
            String message = "Failed to register " + GetUniversityObjectRequest.class.getCanonicalName() + " subtypes";
            log.error(message, e);
            throw new ObjectRequestException(message, e);
        }
    }

    public static GetUniversityObjectRequest create(DataSource dataSource, long objectId) {
        UniversityObject object = new MyUniversityObject(dataSource, objectId);
        UniversityObjectClass objectClazz = object.clazz();
        Class<? extends GetUniversityObjectRequest> requestObjectClass = REQUEST_SUBCLASSES.get(objectClazz);
        try {
            GetUniversityObjectRequest requestObject = requestObjectClass.getConstructor().newInstance();
            requestObject.dataSource = dataSource;
            requestObject.objectId = objectId;
            return requestObject;
        } catch (ReflectiveOperationException e) {
            String message = "Failed to create instance of type " + objectClazz + " subtypes";
            log.error(message, e);
            throw new ObjectRequestException(message, e);
        }
    }

    public abstract UniversityObjectModel execute();
}
