import React from 'react'

import './Input.css'

const Input = ({id, label, value, onChange, disabled = false}) => {
    return (
        <div>
            <label htmlFor={id}>{label}</label>
            <input id={id} value={value} onChange={onChange} disabled={disabled} className="odm-input">
            </input>
        </div>
    );
}

export default Input;
