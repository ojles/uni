import React from 'react'
import Input from './Input'
import UniversityObjectForm from './UniversityObjectForm'
import FormWrapper from './FormWrapper'

const LinkForm = ({object, inputChangeCallback}) => {
    const handleInputChange = (event) => {
        const {id, value} = event.target;
        inputChangeCallback(id, value);
    }

    if (!object.url) {
        object.url = '';
    }

    return (
        <div>
            <FormWrapper text="University Object">
                <UniversityObjectForm object={object} inputChangeCallback={inputChangeCallback}/>
            </FormWrapper>
            <Input id="url" label="URL" value={object.url} onChange={handleInputChange}/>
        </div>
    );
}

export default LinkForm;
