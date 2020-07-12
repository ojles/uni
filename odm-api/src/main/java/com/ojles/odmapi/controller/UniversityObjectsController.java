package com.ojles.odmapi.controller;

import com.ojles.odmapi.configuration.DbConfiguration;
import com.ojles.odmapi.db.ConstUniversityObjects;
import com.ojles.odmapi.db.MyUniversityObjects;
import com.ojles.odmapi.db.UniversityObjects;
import com.ojles.odmapi.payload.AddUniversityObjectRequest;
import com.ojles.odmapi.payload.GetUniversityObjectRequest;
import com.ojles.odmapi.payload.UniversityObjectModel;
import com.ojles.odmapi.payload.UpdateUniversityObjectRequest;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.stream.Collectors;

@RestController
public class UniversityObjectsController {
    @GetMapping("/objects")
    public List<UniversityObjectModel> getObjects(@RequestParam(name = "majorId", required = false) Long majorId) {
        ConstUniversityObjects constUniversityObjects = new ConstUniversityObjects(DbConfiguration.getDataSource());
        if (majorId == null) {
            return constUniversityObjects.roots().stream()
                    .map(UniversityObjectModel::new)
                    .collect(Collectors.toList());
        } else {
            return constUniversityObjects.childrenOf(majorId).stream()
                    .map(UniversityObjectModel::new)
                    .collect(Collectors.toList());
        }
    }

    @GetMapping("/objects/{objectId}")
    public UniversityObjectModel getObjectById(@PathVariable("objectId") Long objectId) {
        return GetUniversityObjectRequest
                .create(DbConfiguration.getDataSource(), objectId)
                .execute();
    }

    @PostMapping("/objects")
    public UniversityObjectModel update(@RequestBody UpdateUniversityObjectRequest updateRequest) {
        return updateRequest.execute(DbConfiguration.getDataSource());
    }

    @PutMapping("/objects")
    public UniversityObjectModel add(@RequestBody AddUniversityObjectRequest addRequest) {
        return addRequest.execute(DbConfiguration.getDataSource());
    }

    @DeleteMapping("/objects/{objectId}")
    public void removeById(@PathVariable("objectId") Long objectId) {
        UniversityObjects objects = new MyUniversityObjects(DbConfiguration.getDataSource());
        objects.deleteById(objectId);
    }
}
