import React from 'react'

const Button = ({content, onClick}) => {
    return (
        <button type="button" onClick={onClick}>{content}</button>
    );
};

export default Button;
