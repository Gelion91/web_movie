from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    id = '__B3kJ8YhSw'
    return render_template('index.html', id=id)


@app.route('/hello', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        result = request.form['search']
        result = result.split('=')
        id = result[-1]
        return render_template('index.html', id=id)


if __name__ == '__main__':
    app.run(debug=True)