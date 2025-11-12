from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/soil')
def soil():
    return render_template('soil.html')

@app.route('/animals')
def animals():
    return render_template('animals.html')

@app.route('/animals/<category>')
def animal_category(category):
    return render_template('animal_category.html', category=category)

if __name__ == '__main__':
    app.run(host='0.0.0.0')