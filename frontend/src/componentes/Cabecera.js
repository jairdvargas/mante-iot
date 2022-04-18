import React from 'react';
import Navbar from 'react-bootstrap/Navbar';

const Cabecera = ({titulo}) => {
    return (
        <Navbar bg="dark" variant="dark">
            <Navbar.Brand href="#home"> {titulo} </Navbar.Brand>
        </Navbar>
    )
};

export default Cabecera;