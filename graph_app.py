from auto_diff import *
import re
from flask import Flask, render_template, request, send_file
from flask_cors import CORS
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
from mpl_toolkits.mplot3d import Axes3D
import random 

app = Flask(__name__)
CORS(app)
@app.route('/', methods=['POST'])
def index():
    variables_str = request.form['variables']
    eval_values = request.form['eval_values']
    dims = int(request.form['dims'])
    function = request.form['function']

    allowed_names = {"Log", "Sin", "Cos", "Variable", "Constant", "Add", "Subtract", "Multiply", "Divide", "+", "-", "*", "/"}
    for i in range(97, 123):
        allowed_names.add(chr(i))
    
    for i in range(65, 91):
        allowed_names.add(chr(i))

    symbols = re.findall(r'\b\w+\b', function)

    # Check if all symbols are allowed to prevent misuse of program
    for symbol in symbols:
        try:
            symbol = float(symbol)
            continue
        except:
            pass
        if symbol not in allowed_names:
            return f"'{symbol}' is not an allowed symbol.", \
            "Use \"Log\", \"Sin\", \"Cos\", \"Variable\", \"Constant\", \"Add\", \"Subtract\", \"Multiply\", \"Divide\", or any of the four operators."

    if dims == 2:
        center = int(eval_values)
        start = max(center - 250, 1)
        end = center + 250
        
        val_arr = np.linspace(start, end, 1000)

        output_arr = []

        partial_arr = []
        for i, val in enumerate(val_arr):
            variables = {}
            variables[variables_str] = val
            output, partial = get_function_outputs(variables, function)

            if not output or not partial:
                val_arr = np.delete(val_arr, i)
                continue

            partial = partial[0]

            output_arr.append(output)
            partial_arr.append(partial)

        output_arr = np.array(output_arr)
        partial_arr = np.array(partial_arr)

        forward_fig, forward_ax = plt.subplots()
        forward_ax.plot(val_arr, output_arr)

        partial_fig, partial_ax = plt.subplots()
        partial_ax.plot(val_arr, partial_arr)

        forward_fig.savefig("forward.png")
        partial_fig.savefig("partial.png")

        forward = Image.open("forward.png")
        partial = Image.open("partial.png")

        fw, fh = forward.size
        pw, ph = partial.size

        width = fw+pw
        height = max(ph, fh)
        combined = Image.new("RGB", (width, height), "white")
        combined.paste(forward, (0,0))
        combined.paste(partial, (fw, 0))
        combined.save("combined.png")

        return send_file('combined.png', mimetype='image/png')

    elif dims == 3:
        vars = variables_str.split(",")
        vars = [var.strip() for var in vars]
        center_x, center_y = eval_values.split(",")
        center_x, center_y = center_x.strip(), center_y.strip()
        center_x, center_y = int(center_x), int(center_y)
        start_x, end_x = max(1, center_x-250), center_x+250
        start_y, end_y = max(1, center_y-250), center_y+250

        num_points = 10000
        x_vals = [random.uniform(start_x, end_x) for _ in range(num_points)]
        y_vals = [random.uniform(start_y, end_y) for _ in range(num_points)]

        grads = []
        outputs = []
        for i in range(len(x_vals)):
            variables = {}
            try:
                variables[vars[0]] = x_vals[i]
                variables[vars[1]] = y_vals[i]
            except:
                break

            output, partials = get_function_outputs(variables, function)

            if not output or not partials:
                x_vals = np.delete(x_vals, i)
                y_vals = np.delete(y_vals, i)
                continue
            
            partials = np.array(partials)
            grads.append(partials)
            outputs.append(output)
        
        grads = np.array(grads)
        outputs = np.array(outputs)

        x_grads = grads[:,0]
        y_grads = grads[:,1]

        ref_point = np.array([0, 0, 0])
        distances = np.linalg.norm(np.column_stack((x_vals, y_vals, outputs)) - ref_point, axis=1)
        colormap = plt.cm.get_cmap('viridis')

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(x_vals, y_vals, outputs, c=distances, cmap=colormap)
        ax.set_title('Input Function')
        plt.savefig("3d.png")
        
        return send_file('3d.png', mimetype='image/png')

def get_function_outputs(variables: dict, function: str):
    a = Graph()

    for_function = {}
    for variable in variables:
        for_function[variable] = Variable(variables.get(variable),variable)
    
    try:
        output = eval(function, None, for_function)
    except Exception as e:
        return None, None
    forward_output = None

    try:
        forward_output = forward_pass()
        backward_pass()
    except Exception as e:
        return None, None
    
    partials = get_partials()
    partials = [partial[1] for partial in partials]

    return forward_output, partials

if __name__ == '__main__':
    app.run(debug=True)