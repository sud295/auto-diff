import './App.css';
import { useState, useEffect } from 'react';
import { isMobile } from 'react-device-detect';

function App() {
  const [variables, setVars] = useState("x");
  const [values, setVals] = useState("2");
  const [func, setFunc] = useState("Log(x)+Sin(x)");
  const [selectedInput, setSelectedInput] = useState("VariableInput"); 
  const [funcOut, setFuncOut] = useState("");
  const [partOut, setPartOut] = useState("");

  const handleInputSelect = (inputType) => {
    setSelectedInput(inputType);
  };

  const handleGraphClick = () => {
    if (variables.length === 0){
      return;
    }
    if (values.length === 0){
      return;
    }
    if (func.length === 0){
      return;
    }
    let function_str = "";
    let visited_indices = [];
    let dimensions = "";

    if (variables.length == 1){
      dimensions = "2";
    }
    else{
      return;
    }

    for (let i = 0; i < func.length; i++) {
      let element = func[i];

      if (visited_indices.includes(i)) {
        continue;
      }

      if (element === "^") {
        function_str += "**";
      } 
      else if (!isNaN(element)) {
        let total_num = element;

        for (let j = i + 1; j < func.length; j++) {
          visited_indices.push(j);

          if (!isNaN(func[j])) {
            total_num += func[j];
          } else {
            visited_indices.pop();
            break;
          }
        }

        function_str += `Constant(${total_num})`;
      }
      else {
        function_str += element;
      }
    }
  
    const formData = new FormData();
    formData.append('variables', variables);
    formData.append('eval_values', values);
    formData.append('function', function_str);
    formData.append('dims', dimensions)
    
    fetch("http://127.0.0.1:8000", {
      method: "POST",
      body: formData,
    })
    .then((response) => response.blob())
    .then((blob) => {
      const imageUrl = URL.createObjectURL(blob);
      const imageElement = document.createElement('img');
      imageElement.src = imageUrl;
      
      const imageContainer = document.getElementById('imageContainer');

      while (imageContainer.firstChild) {
        imageContainer.removeChild(imageContainer.firstChild);
      }

      imageContainer.classList.add('image-container');

      imageContainer.appendChild(imageElement);
    })
    .catch((error) => {
      console.error("Error loading the image:", error);
    });
  }

  const handleCalculateClick = () => {
    if (variables.length === 0){
      return;
    }
    if (values.length === 0){
      return;
    }
    if (func.length === 0){
      return;
    }
    let function_str = "";
    let visited_indices = [];

    for (let i = 0; i < func.length; i++) {
      let element = func[i];

      if (visited_indices.includes(i)) {
        continue;
      }

      if (element === "^") {
        function_str += "**";
      } 
      else if (!isNaN(element)) {
        let total_num = element;

        for (let j = i + 1; j < func.length; j++) {
          visited_indices.push(j);

          if (!isNaN(func[j])) {
            total_num += func[j];
          } else {
            visited_indices.pop();
            break;
          }
        }

        function_str += `Constant(${total_num})`;
      }
      else {
        function_str += element;
      }
    }
  
    const formData = new FormData();
    formData.append('variables', variables);
    formData.append('eval_values', values);
    formData.append('function', function_str);
    
    fetch("https://api.sisha.dev/", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        setFuncOut(data.forward);
        setPartOut(data.partials);
      })
  }

  const handleButtonClick = (value) => {
    if (selectedInput === "VariableInput") {
      if (variables.length === 0){
        setVars(value);
      }
      else if (value === ","){
        setVars(variables + ", ");
      }
      else{
        //setVars(variables + ", " + value);
        setVars(variables + value);
      }

    } 
    else if (selectedInput === "ValueInput") {
      if (values.length === 0){
        setVals(value);
      }
      else if (value === ","){
        setVals(values + ", ");
      }
      else{
        //setVals(values + ", " + value);
        setVals(values + value);
      }
    } 
    else if (selectedInput === "FunctionInput") {
      setFunc(func + value);
    }
  };

  const handleClearClick = () => {
    setFunc("");
    setVals("");
    setVars("");
    setFuncOut("");
    setPartOut("");
  };

  const [activeGroup, setActiveGroup] = useState('Operators');

  const handleGroupChange = (group) => {
    setActiveGroup(group);
  };

  useEffect(() => {
    const handleKeyDown = (event) => {
      const key = event.key;
      if (key === "Backspace"){
        if (selectedInput === "VariableInput"){
          if (variables.charAt(variables.length - 1) === ' '){
            setVars(variables.slice(0, -2));
          }
          else{
            setVars(variables.slice(0, -1));
          }
        }
        else if (selectedInput === "ValueInput"){
          if (values.charAt(values.length - 1) === ' '){
            setVals(values.slice(0, -2));
          }
          else{
            setVals(values.slice(0, -1));
          }
        }
        else{
          setFunc(func.slice(0, -1));
        }
      }
      else if (key === "Shift" || key === "Meta" || key === " "){
        
      }
      else{
        handleButtonClick(key);
      }
    };
  
    window.addEventListener('keydown', handleKeyDown);
  
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [selectedInput, variables, values, func, handleButtonClick]);

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

  if (isMobile) {
    return (
      <div>
        <p>This application is not available on mobile devices.</p>
      </div>
    );
  }

  return (
    <div className="App">
      <div className='userEntries'>
        <div className='VariableInput' onClick={() => handleInputSelect("VariableInput")}>
          {variables || "Click To Enter Variables (Comma Separated)"}
        </div>
        <div className='ValueInput' onClick={() => handleInputSelect("ValueInput")}>
          {values || "Click To Enter Values To Evaluate At (Comma Separated)"}
        </div>
        <div className='FunctionInput' onClick={() => handleInputSelect("FunctionInput")}>
          {func || "Click To Enter Function"}
        </div>
      </div>
  
      <div className="Keypad">
        <div className='GroupSelector'>
          <button onClick={() => handleGroupChange('Digits')}>Digits</button>
          <button onClick={() => handleGroupChange('Operators')}>Operators</button>
          <button onClick={() => handleGroupChange('Variables')}>Variables</button>
        </div>
        {activeGroup === 'Operators' && (
          <div className="Operators">
            <button onClick={() => handleButtonClick('Log')}>Log</button>
            <button onClick={() => handleButtonClick('Sin')}>Sin</button>
            <button onClick={() => handleButtonClick('Cos')}>Cos</button>
            <button onClick={() => handleButtonClick('+')}>+</button>
            <button onClick={() => handleButtonClick('-')}>-</button>
            <button onClick={() => handleButtonClick('/')}>/</button>
            <button onClick={() => handleButtonClick('*')}>*</button>
            <button onClick={() => handleButtonClick('^')}>^</button>
            <button onClick={() => handleButtonClick('(')}>(</button>
            <button onClick={() => handleButtonClick(')')}>)</button>
          </div>
        )}
        {activeGroup === 'Digits' && (
          <div className="Numbers">
            {importNumbers()}
          </div>
        )}
        {activeGroup === 'Variables' && (
          <div className="Variables">
            {importVariables()}
          </div>
        )}
        <div className="calculate">
          <button onClick={handleCalculateClick}>Calculate</button>
          <button onClick={handleClearClick}>Clear</button>
          <button onClick={handleGraphClick}>Graph (2D Only)</button>
        </div>
      </div>

      <div className='Outputs'>
        <div className='FuncOut'>
          {funcOut || "Function Output"}
        </div>
        <div className='PartOut'>
          {partOut || "Partial Derivatives"}
        </div>
        <div id="imageContainer"></div>
      </div>
    </div>
  );
}

export default App;
