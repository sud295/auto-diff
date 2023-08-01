from auto_diff import *
from flask import Flask, render_template, request

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
        
        partials = calculate_partials(variables, function)

        return render_template('index.html', partials=partials)
    
    return render_template('index.html')

def calculate_partials(variables: dict, function: list[str]):
    Graph()

    for_function = {}
    for variable in variables:
        for_function[variable] = Variable(variables.get(variable),variable)
    
    output = eval(function, for_function)

    backward_pass()

    partials = get_partials()

    return partials

if __name__ == '__main__':
    app.run(debug=True)