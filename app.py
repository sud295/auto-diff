from auto_diff import *
from flask import Flask, render_template, request
import re

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        variables_str = request.form['variables']
        eval_values = request.form['eval_values']
        function = request.form['function']
        
        variables = {}
        eval_values = eval_values.split(",")
        variables_str = variables_str.split(",")
        if len(variables_str) != len(eval_values):
            return render_template('index.html', partials="ERROR: Enter matching number of variables and values.")
        
        for i,var in enumerate(variables_str):
            try:
                variables[var] = float(eval_values[i])
            except:
                return render_template('index.html', partials="ERROR: Values must be numeric.")
        
        partials, forward_output = calculate_partials(variables, function)

        return render_template('index.html', partials=partials, forward=forward_output)
    
    return render_template('index.html')

def calculate_partials(variables: dict, function: str):
    allowed_names = {"Log", "Sin", "Cos", "Variable", "Constant", "Add", "Subtract", "Multiply", "Divide", "+", "-", "*", "/"}
    for i in range(97, 123):
        allowed_names.add(chr(i))

    Graph()

    for_function = {}
    for variable in variables:
        for_function[variable] = Variable(variables.get(variable),variable)
    
    symbols = re.findall(r'\b\w+\b', function)

    print(symbols)
    # Check if all symbols are allowed to prevent misuse of program
    for symbol in symbols:
        if symbol not in allowed_names:
            return ValueError(f"'{symbol}' is not an allowed symbol."), \
            "Use \"Log\", \"Sin\", \"Cos\", \"Variable\", \"Constant\", \"Add\", \"Subtract\", \"Multiply\", \"Divide\", or any of the four operators."
        
    try:
        output = eval(function, None, for_function)
    except:
        return "That didn't work! Try again.", ""

    forward_output = None
    try:
        forward_output = forward_pass()
        backward_pass()
    except:
        return "That didn't work! Try again.", ""
    
    partials = get_partials()

    out_str = ""
    for partial in partials:
        out_str += str(partial[0])
        out_str += "="
        out_str += str(partial[1])
        out_str += ", "
    
    out_str = out_str[:-2]

    return out_str, forward_output

if __name__ == '__main__':
    app.run(debug=False)