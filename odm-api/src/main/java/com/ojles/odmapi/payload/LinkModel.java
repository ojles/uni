package com.ojles.odmapi.payload;

import com.ojles.odmapi.db.Link;
import lombok.Getter;
import lombok.Setter;

import java.time.LocalDate;

@Getter
@Setter
public class LinkModel extends UniversityObjectModel {
    private String url;

    public LinkModel(Link link) {
        super(link);
        this.url = link.url();
    }
}
