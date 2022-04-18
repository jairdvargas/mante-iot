import React from 'react';
import Badge from 'react-bootstrap/Badge';

const Variabledigital = ({nombretag, valortag}) => {
    console.log("Componente renderizado variable digital");
    return (
        <h2>
            {nombretag} : <Badge pill bg="success"> {valortag} </Badge>
        </h2>
    )
};

export default Variabledigital;