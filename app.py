from flask import Flask, render_template, request
import numpy as np
import ast
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        array1 = request.form['array1']
        array2 = request.form['array2']

        # Convert input strings to arrays
        array1 = ast.literal_eval(array1)
        array2 = ast.literal_eval(array2)

        # Create a plot
        fig, ax = plt.subplots()
        ax.plot(array1, array2)

        # Convert the plot to a base64 string for display
        import io, base64
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        plot_data = base64.b64encode(buf.read()).decode('ascii')

        return render_template('index.html', plot_data=plot_data)
    else:
        return render_template('index.html')

@app.route('/multiply', methods=['GET', 'POST'])
def multiply():
    if request.method == 'POST':
        x = request.form['x']
        y = request.form['y']

        # Convert input strings to arrays
        x = ast.literal_eval(x)
        y = ast.literal_eval(y)

        # Multiply the arrays
        result = np.dot(x, y)

        return render_template('mul.html', result=result)
    else:
        return render_template('mul.html')


if __name__ == '__main__':
    app.run(debug=True)
