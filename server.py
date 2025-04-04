from flask import Flask, request, jsonify, render_template_string
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Initialize SQLite database
def init_db():
    with sqlite3.connect('sensor_data.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS sensor_data (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            temperature REAL,
                            humidity REAL,
                            pressure REAL,
                            altitude REAL,
                            dustDensity REAL,
                            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                        )''')
        conn.commit()

# Insert sensor data into the database
def insert_sensor_data(temperature, humidity, pressure, altitude, dustDensity):
    with sqlite3.connect('sensor_data.db') as conn:
        conn.execute('''INSERT INTO sensor_data (temperature, humidity, pressure, altitude, dustDensity)
                        VALUES (?, ?, ?, ?, ?)''', 
                     (temperature, humidity, pressure, altitude, dustDensity))
        conn.commit()

# Route to accept sensor data via POST
@app.route('/api/sensor_data', methods=['POST'])
def sensor_data():
    data = request.get_json()

    if not data or 'temperature' not in data or 'humidity' not in data or 'pressure' not in data or 'altitude' not in data or 'dustDensity' not in data:
        return jsonify({'error': 'Missing data'}), 400
    
    temperature = data['temperature']
    humidity = data['humidity']
    pressure = data['pressure']
    altitude = data['altitude']
    dustDensity = data['dustDensity']
    
    insert_sensor_data(temperature, humidity, pressure, altitude, dustDensity)
    
    return jsonify({'message': 'Data received successfully'}), 200

# Route to display the sensor data in a simple HTML page
@app.route('/')
def index():
    with sqlite3.connect('sensor_data.db') as conn:
        cursor = conn.execute('SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 10')
        rows = cursor.fetchall()
    
    html_content = '''
    <html>
        <head>
            <title>Sensor Data</title>
        </head>
        <body>
            <h1>Latest Sensor Data</h1>
            <div id="sensor-data">
                <table border="1">
                    <tr>
                        <th>Temperature</th>
                        <th>Humidity</th>
                        <th>Pressure</th>
                        <th>Altitude</th>
                        <th>Dust Density</th>
                        <th>Timestamp</th>
                    </tr>
    '''
    
    for row in rows:
        html_content += f'''
        <tr>
            <td>{row[1]}</td>
            <td>{row[2]}</td>
            <td>{row[3]}</td>
            <td>{row[4]}</td>
            <td>{row[5]}</td>
            <td>{row[6]}</td>
        </tr>
        '''
    
    html_content += '''
                </table>
            </div>
        </body>
    </html>
    '''
    
    return render_template_string(html_content)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
