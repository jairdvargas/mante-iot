import 'bootstrap/dist/css/bootstrap.min.css';
import React from 'react';
import { useState, useEffect, useRef } from 'react';
import { Container, Row, Col, Tab, Tabs} from 'react-bootstrap';
import Actualizar from './componentes/Actualizar';
import Variableanalogica from './componentes/Variableanalogica';
import Variabledigital from './componentes/Variabledigital';
import Cabecera from './componentes/Cabecera';

const API_URL = 'http://127.0.0.1:5051';

const App = () => {
  
  const [variable, definirVariable] = useState([]);
  //solo se ejecutara una sola vez para leer un solo tag simulado
  const getVariableInstantanea = () => {
    try {
      const resultado = 100.1234 + Math.random();
      definirVariable(resultado);
    } catch (error) {
      console.log(error);
    }
  };

  //--- inicio No recuerdo para que sirve
  const AuxValor1 = variable ? variable : 0.0000;
  //--- fin No recuerdo para que sirve

  useEffect(() => getVariableInstantanea(), []);
  //console.log(variable);
  //console.log(variable.Valor);

  //-----------Boton de actualizar valor
  const Actualiza1Variable = (id) => {
    console.log("click detectado")
    try {
      const resultado = 200.1234 + Math.random();
      definirVariable(resultado);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div className="App">
      <Cabecera titulo="Variables de proceso" />
      <Tabs defaultActiveKey="home" id="uncontrolled-tab-example" className="mb-3">
        <Tab eventKey="home" title="Home">
		      <p> tab1 </p>
        </Tab>
        <Tab eventKey="profile" title="Profile">
          <Actualizar eliminarValorAnterior={Actualiza1Variable}/>
          <Variableanalogica nombretag="Flujo de balanza: " valortag={AuxValor1} unidadtag=" Kg/h" />
          <Variabledigital  nombretag="Estado de Planta " valortag="Funcionando" />
        </Tab>
        <Tab eventKey="Historicos" title="Contact">
		      <p> tab2 </p>
        </Tab>
      </Tabs>
    </div>
  );
}

export default App;
