package com.ojles.odmapi.payload;

import com.ojles.odmapi.db.*;
import lombok.Getter;
import lombok.Setter;

import javax.sql.DataSource;
import java.time.LocalDate;

@Getter
@Setter
public class AddLinkRequest extends AddUniversityObjectRequest {
    private String url;

    @Override
    public LinkModel execute(DataSource dataSource) {
        Links links = new MyLinks(dataSource);
        long generatedId = links.insert(
                getName(),
                UniversityObjectClass.LINK,
                getMajorId(),
                url
        );
        links = new ConstLinks(dataSource);
        Link link = links.byId(generatedId);
        return new LinkModel(link);
    }

    @Override
    public UniversityObjectClass clazz() {
        return UniversityObjectClass.LINK;
    }
}
