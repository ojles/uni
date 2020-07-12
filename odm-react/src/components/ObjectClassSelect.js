import React from 'react'

const ObjectClassSelect = ({value, optionChangeCallback}) => {
    return (
        <select value={value} defaultValue="" onChange={optionChangeCallback}>
            <option value="" disabled>Choose class</option>
            <option value="PERSON">Person</option>
            <option value="DEPARTMENT">Department</option>
            <option value="DIVISION">Division</option>
            <option value="FACULTY">Faculty</option>
            <option value="LINK">Link</option>
        </select>
    );
}

export default ObjectClassSelect;
