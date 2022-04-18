import React from 'react';
import Badge from 'react-bootstrap/Badge';


const Variableanalogica = ({nombretag, valortag, unidadtag}) => {
    console.log("Componente renderizado variable analogica");
    return (
        <h2> {nombretag} 
        <Badge bg="primary">
            {valortag}
            {unidadtag}
            </Badge>
        </h2>
    )
};

export default Variableanalogica;