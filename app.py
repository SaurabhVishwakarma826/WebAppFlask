from flask import Flask, render_template, request
import numpy as np
import ast
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        array1 = request.form.get('array1', '').strip()
        array2 = request.form.get('array2', '').strip()

        # Check that arrays are not empty
        if not array1 or not array2:
            error_msg = "Please enter values for both arrays."
            return render_template('index.html', error_msg=error_msg)

        # Convert input strings to arrays
        try:
            array1 = ast.literal_eval(array1)
            array2 = ast.literal_eval(array2)
        except:
            error_msg = "Please enter valid arrays."
            return render_template('index.html', error_msg=error_msg)

        # Check that arrays have the same length
        if len(array1) != len(array2):
            error_msg = "Arrays must have the same length."
            return render_template('index.html', error_msg=error_msg)

        # Create a plot
        fig, ax = plt.subplots()
        ax.plot(array1, array2)
        plt.title("X vs Y plot")
        plt.xlabel("X")
        plt.ylabel("Y")

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
        try:
            x = ast.literal_eval(x)
            y = ast.literal_eval(y)
        except ValueError:
            error_msg = "Error: Invalid input format. Please enter comma-separated values within square brackets."
            return render_template('mul.html', error_msg=error_msg)

        # Check if x and y have the same dimensions
        if len(x[0]) != len(y):
            error_msg = "Error: Dimensions of x and y are not compatible for matrix multiplication."
            return render_template('mul.html', error_msg=error_msg)

        # Multiply the arrays
        res = np.dot(x, y)
        result = ""
        for row in res:
            for elem in row:
                result += str(elem)+', '
            result = result[:-2]+"\n"

        return render_template('mul.html', result=result)
    else:
        return render_template('mul.html')



if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
