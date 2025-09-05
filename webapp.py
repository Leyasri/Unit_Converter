from flask import Flask, request, render_template_string

app = Flask(__name__)

# Back-end: Unit definitions and conversion logic
units = {
    'Length': ['meters', 'kilometers', 'centimeters', 'millimeters', 'miles', 'feet', 'inches', 'yards'],
    'Weight': ['kilograms', 'grams', 'milligrams', 'metric tons', 'pounds', 'ounces'],
    'Temperature': ['celsius', 'fahrenheit', 'kelvin', 'rankine'],
    'Volume': ['liters', 'milliliters', 'gallons', 'cubic meters']
}

def convert_length(value, from_unit, to_unit):
    length_units = {
        'meters': 1.0, 'kilometers': 1000.0, 'centimeters': 0.01, 'millimeters': 0.001,
        'miles': 1609.34, 'feet': 0.3048, 'inches': 0.0254, 'yards': 0.9144
    }
    if from_unit not in length_units or to_unit not in length_units:
        return None
    result = value * length_units[from_unit] / length_units[to_unit]
    return round(result, 4)

def convert_weight(value, from_unit, to_unit):
    weight_units = {
        'kilograms': 1.0, 'grams': 0.001, 'milligrams': 0.000001, 'metric tons': 1000.0,
        'pounds': 0.453592, 'ounces': 0.0283495
    }
    if from_unit not in weight_units or to_unit not in weight_units:
        return None
    result = value * weight_units[from_unit] / weight_units[to_unit]
    return round(result, 4)

def convert_temperature(value, from_unit, to_unit):
    if from_unit == 'celsius' and to_unit == 'fahrenheit':
        return round((value * 9/5) + 32, 4)
    elif from_unit == 'fahrenheit' and to_unit == 'celsius':
        return round((value - 32) * 5/9, 4)
    elif from_unit == 'celsius' and to_unit == 'kelvin':
        return round(value + 273.15, 4)
    elif from_unit == 'kelvin' and to_unit == 'celsius':
        return round(value - 273.15, 4)
    elif from_unit == 'fahrenheit' and to_unit == 'kelvin':
        return round((value - 32) * 5/9 + 273.15, 4)
    elif from_unit == 'kelvin' and to_unit == 'fahrenheit':
        return round((value - 273.15) * 9/5 + 32, 4)
    elif from_unit == 'celsius' and to_unit == 'rankine':
        return round((value + 273.15) * 9/5, 4)
    elif from_unit == 'rankine' and to_unit == 'celsius':
        return round((value * 5/9) - 273.15, 4)
    elif from_unit == 'fahrenheit' and to_unit == 'rankine':
        return round(value + 459.67, 4)
    elif from_unit == 'rankine' and to_unit == 'fahrenheit':
        return round(value - 459.67, 4)
    elif from_unit == 'kelvin' and to_unit == 'rankine':
        return round(value * 9/5, 4)
    elif from_unit == 'rankine' and to_unit == 'kelvin':
        return round(value * 5/9, 4)
    elif from_unit == to_unit:
        return round(value, 4)
    return None

def convert_volume(value, from_unit, to_unit):
    volume_units = {
        'liters': 1.0, 'milliliters': 0.001, 'gallons': 3.78541, 'cubic meters': 1000.0
    }
    if from_unit not in volume_units or to_unit not in volume_units:
        return None
    result = value * volume_units[from_unit] / volume_units[to_unit]
    return round(result, 4)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""
    error = ""
    selected_category = request.form.get('category', 'Length')
    from_unit = request.form.get('from_unit', units[selected_category][0])
    to_unit = request.form.get('to_unit', units[selected_category][1] if len(units[selected_category]) > 1 else units[selected_category][0])
    value = request.form.get('value', '')

    if request.method == 'POST':
        try:
            value = float(request.form['value'])
            category = request.form['category']
            from_unit = request.form['from_unit']
            to_unit = request.form['to_unit']
            if category == 'Length':
                result_value = convert_length(value, from_unit, to_unit)
            elif category == 'Weight':
                result_value = convert_weight(value, from_unit, to_unit)
            elif category == 'Temperature':
                result_value = convert_temperature(value, from_unit, to_unit)
            elif category == 'Volume':
                result_value = convert_volume(value, from_unit, to_unit)
            else:
                result_value = None
            if result_value is None:
                error = "Invalid unit conversion."
            else:
                result = f"Result: {result_value} {to_unit.capitalize()}"
        except ValueError:
            error = "Please enter a valid number."

    # HTML template with mobile-optimized styling
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Unit Converter</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {
                font-family: Arial, sans-serif;
                padding: 20px;
                max-width: 600px;
                margin: auto;
                background-color: #f4f4f4;
            }
            h2 {
                text-align: center;
                color: #333;
            }
            select, input[type="text"], button {
                font-size: 18px;
                padding: 12px;
                margin: 8px 0;
                width: 100%;
                box-sizing: border-box;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            button {
                background-color: #4CAF50;
                color: white;
                border: none;
                cursor: pointer;
            }
            button:hover {
                background-color: #45a049;
            }
            .error {
                color: red;
                font-size: 16px;
            }
            .result {
                font-size: 18px;
                color: #333;
                margin-top: 10px;
            }
        </style>
        <script>
            function updateUnits() {
                document.getElementById('unitForm').submit();
            }
        </script>
    </head>
    <body>
        <h2>Unit Converter</h2>
        <form id="unitForm" method="post">
            <label>Category:</label><br>
            <select name="category" onchange="updateUnits()">
                {% for cat in units.keys() %}
                <option value="{{ cat }}" {% if cat == selected_category %}selected{% endif %}>{{ cat }}</option>
                {% endfor %}
            </select><br>
            <label>Value:</label><br>
            <input type="text" name="value" placeholder="Enter value" value="{{ value }}"><br>
            <label>From:</label><br>
            <select name="from_unit">
                {% for unit in units[selected_category] %}
                <option value="{{ unit }}" {% if unit == from_unit %}selected{% endif %}>{{ unit }}</option>
                {% endfor %}
            </select><br>
            <label>To:</label><br>
            <select name="to_unit">
                {% for unit in units[selected_category] %}
                <option value="{{ unit }}" {% if unit == to_unit %}selected{% endif %}>{{ unit }}</option>
                {% endfor %}
            </select><br>
            <button type="submit">Convert</button>
        </form>
        <p class="result">{{ result }}</p>
        <p class="error">{{ error }}</p>
    </body>
    </html>
    '''
    return render_template_string(html, units=units, result=result, error=error, selected_category=selected_category, value=value, from_unit=from_unit, to_unit=to_unit)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)