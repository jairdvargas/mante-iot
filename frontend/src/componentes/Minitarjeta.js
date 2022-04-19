import React from 'react';
import ProgressBar from 'react-bootstrap/ProgressBar';
import Card from 'react-bootstrap/Card'

const Minitarjeta = ({variableHist}) => {
    //console.log(variableHist);
    const valor=Number(variableHist.valor);
    const minimo=Number(variableHist.egu_min);
    const maximo=Number(variableHist.egu_max);
    const rango=maximo-minimo;
    const inicio=valor-minimo;
    const barraporciento= (inicio*100)/rango;
    console.log(barraporciento);
    //const barra = ((Number(variableHist.valor)- Number(variableHist.egu_min)) * 100) / (Number(variableHist.egu_max) - Number(variableHist.egu_min));
    
    return (
        <Card style={{ width: '18rem' }}>
            <Card.Body>
                <Card.Title>{variableHist.descripcion?.toUpperCase()}</Card.Title>
                <Card.Subtitle className="mb-2 text-muted">{variableHist.nombre}</Card.Subtitle>
                <Card.Text>
                {variableHist.valor} {' '} {variableHist.egu_unidad}
                </Card.Text>
                <ProgressBar variant="success" now={barraporciento} label={`${barraporciento}%`} />
            </Card.Body>
            <Card.Footer>
                <small className="text-muted">{'Ultima actualización: '} {variableHist.fechalectura} </small>
            </Card.Footer>
        </Card>

    )
};

export default Minitarjeta;