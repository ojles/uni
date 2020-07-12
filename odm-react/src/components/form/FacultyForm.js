import React from 'react'
import Input from './Input'
import DepartmentForm from './DepartmentForm'
import FormWrapper from './FormWrapper'

const FacultyForm = ({object, inputChangeCallback}) => {
    const handleInputChange = (event) => {
        const {id, value} = event.target;
        inputChangeCallback(id, value);
    }

    if (!object.address) {
        object.address = '';
    }

    return (
        <div>
            <FormWrapper text="Department">
                <DepartmentForm object={object} inputChangeCallback={inputChangeCallback}/>
            </FormWrapper>
            <Input id="address" label="Address" value={object.address} onChange={handleInputChange}/>
        </div>
    );
}

export default FacultyForm;
