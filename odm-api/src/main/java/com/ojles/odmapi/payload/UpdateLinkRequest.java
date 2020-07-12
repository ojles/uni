package com.ojles.odmapi.payload;

import com.ojles.odmapi.db.*;
import lombok.Getter;
import lombok.Setter;

import javax.sql.DataSource;
import java.time.LocalDate;

@Getter
@Setter
public class UpdateLinkRequest extends UpdateUniversityObjectRequest {
    private String url;

    @Override
    public LinkModel execute(DataSource dataSource) {
        Link link = new MyLink(dataSource, getId());
        link.update(getName(), url);
        Links links = new ConstLinks(dataSource);
        link = links.byId(getId());
        return new LinkModel(link);
    }

    @Override
    public UniversityObjectClass clazz() {
        return UniversityObjectClass.LINK;
    }
}
