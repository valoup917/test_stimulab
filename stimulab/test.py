from flask import Flask, request, render_template, jsonify, redirect, url_for
import csv

app = Flask(__name__)

@app.route('/')
def index():
    data = []
    with open('discussion.csv', 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            data.append(row)
    return render_template('index.html', data=data)

@app.route('/add_data', methods=['POST'])
def add_data():
    name = request.form.get('name')
    theme = request.form.get('theme')
    private = request.form.get('private')
    message = request.form.get('message')

    if (private == None):
        private = "Public"
    if (private == 'on'):
        private = "Private"

    if not all([name, theme, private, message]):
        return jsonify({'error': 'All fields are required'}), 400
    try:
        with open('discussion.csv', 'a') as file:
            file.write("\n" + '"' + name + '"' + ',' + '"' + theme + '"' + ',' + '"' + private + '"' + ',' + '"' + message + '"')
            #csvwriter = csv.writer(file)
            #csvwriter.writerow([name, theme, private, message])
    except Exception as e:
        return jsonify({'error': 'Error while adding data to csv'}), 500
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)