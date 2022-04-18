import React from 'react';
import Button from 'react-bootstrap/Button';

const Actualizar = ({ eliminarValorAnterior}) => {
  //vamos a retornar descripcion o sino alt descripcion porque a veces viene en null
  console.log("Componente renderizado");
  return (
    <Button variant="primary" onClick={() => eliminarValorAnterior("Tagnuevo")}>
      Actualizar
    </Button>
  );
};

export default Actualizar;
  