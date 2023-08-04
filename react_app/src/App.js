import './App.css';
import { useState, useEffect } from 'react';

function App() {
  const [variables, setVars] = useState("");
  const [values, setVals] = useState("");
  const [func, setFunc] = useState("");
  const [selectedInput, setSelectedInput] = useState(null); // Track selected input type

  const handleInputSelect = (inputType) => {
    setSelectedInput(inputType);
  };

  const handleButtonClick = (value) => {
    if (selectedInput === "VariableInput") {
      setVars(variables + value);
    } 
    else if (selectedInput === "ValueInput") {
      setVals(values + value);
    } 
    else if (selectedInput === "FunctionInput") {
      setFunc(func + value);
    }
  };

  const handleClearClick = () => {
    setFunc("");
    setVals("");
    setVars("");
  };

  useEffect(() => {
    const handleKeyDown = (event) => {
      const key = event.key;
      if (/[0-9a-zA-Z()+\-*/^]/.test(key)) {
        handleButtonClick(key);
      }
    };

    window.addEventListener('keydown', handleKeyDown);

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [selectedInput]);

  const importNumbers = () => {
    const numbers = [];
    for (let i = 0; i < 10; i++) {
      numbers.push(<button onClick={() => handleButtonClick(i.toString())} key={i}>{i}</button>);
    }
    return numbers;
  }

  const importVariables = () => {
    const variables = [];
    for (let i = 97; i < 123; i++) {
      variables.push(<button onClick={() => handleButtonClick(String.fromCharCode(i))} key={i}>{String.fromCharCode(i)}</button>);
    }
    for (let i = 65; i < 91; i++) {
      variables.push(<button onClick={() => handleButtonClick(String.fromCharCode(i))} key={i}>{String.fromCharCode(i)}</button>);
    }
    return variables;
  }

  return (
    <div className="App">
      <div className='VariableInput' onClick={() => handleInputSelect("VariableInput")}>
        {variables || "Enter Variables"}
      </div>
      <div className='ValueInput' onClick={() => handleInputSelect("ValueInput")}>
        {values || "Enter Values To Evaluate At"}
      </div>
      <div className='FunctionInput' onClick={() => handleInputSelect("FunctionInput")}>
        {func || "Enter Function"}
      </div>
      <div className="AutoDiff">
        <div className="Operators">
          <button onClick={() => handleButtonClick('Log')}>Log</button>
          <button onClick={() => handleButtonClick('Sin')}>Sin</button>
          <button onClick={() => handleButtonClick('Cos')}>Cos</button>
          <button onClick={() => handleButtonClick('Constant')}>Constant</button>
          <button onClick={() => handleButtonClick('+')}>+</button>
          <button onClick={() => handleButtonClick('-')}>-</button>
          <button onClick={() => handleButtonClick('/')}>/</button>
          <button onClick={() => handleButtonClick('*')}>*</button>
          <button onClick={() => handleButtonClick('^')}>^</button>
          <button onClick={() => handleButtonClick('(')}>(</button>
          <button onClick={() => handleButtonClick(')')}>)</button>
        </div>
        <div className="Numbers">
          {importNumbers()}
        </div>
        <div className="Variables">
          {importVariables()}
        </div>
        <div className="calculate">
          <button>Calculate</button>
          <button onClick={handleClearClick}>Clear</button>
        </div>
      </div>
    </div>
  );
}

export default App;
