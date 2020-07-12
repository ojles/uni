import React from 'react'
import Input from './Input'
import DepartmentForm from './DepartmentForm'
import FormWrapper from './FormWrapper'

const DivisionForm = ({object, inputChangeCallback}) => {
    const handleInputChange = (event) => {
        const {id, value} = event.target;
        inputChangeCallback(id, value);
    }

    return (
        <div>
            <FormWrapper text="Department">
                <DepartmentForm object={object} inputChangeCallback={inputChangeCallback}/>
            </FormWrapper>
            <Input id="roomNumber" label="Room number" value={object.roomNumber} onChange={handleInputChange}/>
        </div>
    );
}

export default DivisionForm;
