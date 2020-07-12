package com.ojles.odmapi.payload;

import com.ojles.odmapi.db.ConstLinks;
import com.ojles.odmapi.db.Link;
import com.ojles.odmapi.db.Links;
import com.ojles.odmapi.db.UniversityObjectClass;

public class GetLinkRequest extends GetUniversityObjectRequest {
    @Override
    public UniversityObjectModel execute() {
        Links links = new ConstLinks(dataSource);
        Link link = links.byId(objectId);
        return new LinkModel(link);
    }

    @Override
    public UniversityObjectClass clazz() {
        return UniversityObjectClass.LINK;
    }
}
