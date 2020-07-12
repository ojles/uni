package com.ojles.odmapi.db;

import com.ojles.odmapi.configuration.TestDbConfiguration;
import org.junit.Test;

import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.*;

public class MyUniversityObjectTest {
    @Test
    public void shouldReturnCorrectId() {
        long id = 992L;
        MyUniversityObject universityObject = new MyUniversityObject(TestDbConfiguration.getDataSource(), id);
        assertThat(universityObject.id(), is(id));
    }
}
