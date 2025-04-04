from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Global variable to hold the most recent sensor data
latest_sensor_data = {}

# Route to accept sensor data via POST
@app.route('/api/sensor_data', methods=['POST'])
def sensor_data():
    global latest_sensor_data

    data = request.get_json()

    if not data or 'temperature' not in data or 'humidity' not in data or 'pressure' not in data or 'altitude' not in data or 'dustDensity' not in data:
        return jsonify({'error': 'Missing data'}), 400

    # Store the latest sensor data
    latest_sensor_data = {
        'temperature': data['temperature'],
        'humidity': data['humidity'],
        'pressure': data['pressure'],
        'altitude': data['altitude'],
        'dustDensity': data['dustDensity']
    }

    return jsonify({'message': 'Data received successfully'}), 200

# Route to display the sensor data in a simple HTML page
@app.route('/')
def index():
    if not latest_sensor_data:
        return "No data received yet."
    
    # Create a simple HTML page to display the latest data
    html_content = f'''
    <html>
        <head>
            <title>Latest Sensor Data</title>
        </head>
        <body>
            <h1>Latest Sensor Data</h1>
            <table border="1">
                <tr>
                    <th>Temperature</th>
                    <th>Humidity</th>
                    <th>Pressure</th>
                    <th>Altitude</th>
                    <th>Dust Density</th>
                </tr>
                <tr>
                    <td>{latest_sensor_data['temperature']}</td>
                    <td>{latest_sensor_data['humidity']}</td>
                    <td>{latest_sensor_data['pressure']}</td>
                    <td>{latest_sensor_data['altitude']}</td>
                    <td>{latest_sensor_data['dustDensity']}</td>
                </tr>
            </table>
        </body>
    </html>
    '''
    
    return render_template_string(html_content)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
