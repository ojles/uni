import React from 'react'
import FormWrapper from './FormWrapper'
import UniversityObjectForm from './UniversityObjectForm'
import PersonForm from './PersonForm'
import DepartmentForm from './DepartmentForm'
import FacultyForm from './FacultyForm'
import DivisionForm from './DivisionForm'
import LinkForm from './LinkForm'

const ObjectForm = ({object, inputChangeCallback}) => {
    let FormClass = UniversityObjectForm;
    if (object.clazz === 'PERSON') {
        FormClass = PersonForm;
    } else if (object.clazz === 'DEPARTMENT') {
        FormClass = DepartmentForm;
    } else if (object.clazz === 'FACULTY') {
        FormClass = FacultyForm;
    } else if (object.clazz === 'DIVISION') {
        FormClass = DivisionForm;
    } else if (object.clazz === 'LINK') {
        FormClass = LinkForm;
    }
    return (
        <FormWrapper text={object.clazz}>
            <FormClass object={object} inputChangeCallback={inputChangeCallback}/>
        </FormWrapper>
    );
};

export default ObjectForm;
