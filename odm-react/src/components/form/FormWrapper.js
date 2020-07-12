import React from 'react'
import './FormWrapper.css'

const FormWrapper = ({text, children}) => {
    return (
        <div className="form-wrapper">
        <span className="form-wrapper-text">{text}</span>
            {children}
        </div>
    );
};

export default FormWrapper;
