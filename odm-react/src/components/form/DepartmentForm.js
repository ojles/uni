import React from 'react'
import Input from './Input'
import UniversityObjectForm from './UniversityObjectForm'
import FormWrapper from './FormWrapper'

const DepartmentForm = ({object, inputChangeCallback}) => {
    const handleInputChange = (event) => {
        const {id, value} = event.target;
        inputChangeCallback(id, value);
    }

    if (!object.email) {
        object.email = '';
    }
    if (!object.headOfId) {
        object.headOfId = '';
    }

    return (
        <div>
            <FormWrapper text="University Object">
                <UniversityObjectForm object={object} inputChangeCallback={inputChangeCallback}/>
            </FormWrapper>
            <Input id="headOfId" label="Head of ID" value={object.headOfId} onChange={handleInputChange}/>
            <Input id="email" label="Email" value={object.email} onChange={handleInputChange}/>
        </div>
    );
}

export default DepartmentForm;
