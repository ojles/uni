import React from 'react'
import Input from './Input'

const UniversityObjectForm = ({object, inputChangeCallback}) => {
    const handleInputChange = (event) => {
        const {id, value} = event.target;
        inputChangeCallback(id, value);
    }

    return (
        <div className="odm-object-form">
            <Input id="id" label="Id" value={object.id} onChange={handleInputChange} disabled={true}/>
            <Input id="name" label="Name" value={object.name} onChange={handleInputChange}/>
        </div>
    );
}

export default UniversityObjectForm;
