import 'bootstrap/dist/css/bootstrap.min.css';
import React from 'react';
import { useState, useEffect, useRef } from 'react';
import { Container, Row, Col, Tab, Tabs} from 'react-bootstrap';
import axios from 'axios';
import Actualizar from './componentes/Actualizar';
import Variableanalogica from './componentes/Variableanalogica';
import Variabledigital from './componentes/Variabledigital';
import Cabecera from './componentes/Cabecera';
import Minitarjeta from './componentes/Minitarjeta';

const API_URL = 'http://127.0.0.1:5051';

const App = () => {
  
  //variable simulada para probar la funcionalidad
  const [variable, definirVariable] = useState([]);
  //dato instantanteo del tag o tags desde el api de la pdb 
  const [instantaneo, definirInstantaneo] = useState([]);


  //--00--variable simulada ----solo se ejecutara una sola vez para leer un solo tag simulado
  const getVariableInstantanea = () => {
    try {
      const resultado = 100.1234 + Math.random();
      definirVariable(resultado);
    } catch (error) {
      console.log(error);
    }
  };
  //---00 Pone a cero variable simulada
  const AuxValor1 = variable ? variable : 0.0000;
  //--00- fin No recuerdo para que sirve
  //--00
  useEffect(() => getVariableInstantanea(), []);
  
  //--01--variable instantanea ---- Ejecucion de una sola vez para recuperar tags y valores de servidor
  const getInstantaneo = async () => {
    //const resultado = await axios.get(`${API_URL}/leervaloresPDB`);
    try {
      const resultado = await axios.get(`${API_URL}/leervaloresPDB`);
      definirInstantaneo(resultado.data || [])
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => getInstantaneo(),[]);
  //---fin ---01


  //--00---------Boton de actualizar valor
  const Actualiza1Variable = (id) => {
    console.log("click detectado")
    try {
      const resultado = 200.1234 + Math.random();
      definirVariable(resultado);
    } catch (error) {
      console.log(error);
    }
  };

  //-03----- inicio --- Funcion para actualizar cada x segundos
  useInterval(() => {
    // Se lee cada 1000 milisegundos osea 1 segundo los datos del servidor
    getInstantaneo();
  }, 1000);

  //https://overreacted.io/making-setinterval-declarative-with-react-hooks/
  function useInterval(callback, delay) {
    const savedCallback = useRef();
  
    // Remember the latest callback.
    useEffect(() => {
      savedCallback.current = callback;
    }, [callback]);
  
    // Set up the interval.
    useEffect(() => {
      function tick() {
        savedCallback.current();
      }
      if (delay !== null) {
        let id = setInterval(tick, delay);
        return () => clearInterval(id);
      }
    }, [delay]);
  }
  //--03----- fin


  return (
    <div className="App">
      <Cabecera titulo="Variables de proceso" />
      <Tabs defaultActiveKey="home" id="uncontrolled-tab-example" className="mb-3">
        <Tab eventKey="home" title="Home">
          <Container className="mt-4">
            {instantaneo.length ? (
              <Row sd={1} md={2} lg={3}>
              {instantaneo.map((imagen, i) => (
                <Col key={i} className="pb-3">
                  <Minitarjeta variableHist={imagen} />
                </Col>
              ))}
              </Row>
              ) : (
              <br />
            )}
           </Container>
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
