import React from 'react'
import Input from './Input'
import UniversityObjectForm from './UniversityObjectForm'
import FormWrapper from './FormWrapper'

const PersonForm = ({object, inputChangeCallback}) => {
    const handleInputChange = (event) => {
        const {id, value} = event.target;
        inputChangeCallback(id, value);
    }

    if (!object.birthDate) {
        object.birthDate = '';
    }

    return (
        <div>
            <FormWrapper text="University Object">
                <UniversityObjectForm object={object} inputChangeCallback={inputChangeCallback}/>
            </FormWrapper>
            <Input id="birthDate" label="Birth Date" value={object.birthDate} onChange={handleInputChange}/>
        </div>
    );
}

export default PersonForm;
