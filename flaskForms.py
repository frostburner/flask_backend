from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mysqldb import MySQL

app = Flask(__name__)
CORS(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask_db'  # Update the database name here

mysql = MySQL(app)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.json['name']
    email = request.json['email']
    date = request.json['date']
    quote = request.json['quote']
    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO flaskdb (name, email, date, quote) VALUES (%s, %s, %s, %s)', (name, email, date, quote))  # Update the table name here
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'Quote submitted successfully'})

@app.route('/quotes', methods=['GET'])
def display_quotes():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM flaskdb')  # Update the table name here
    quotes = cursor.fetchall()
    cursor.close()
    return jsonify(quotes)

@app.route('/quotes/<int:quote_id>', methods=['DELETE'])
def delete_quote(quote_id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM flaskdb WHERE id = %s', (quote_id,))  # Update the table name and column name here
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'Quote deleted successfully'})

if __name__ == '__main__':
    app.run(host='localhost', port=3000)