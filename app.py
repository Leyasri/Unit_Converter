from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLineEdit, QPushButton, QLabel
from PyQt5.QtCore import Qt
import sys

class UnitConverterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Unit Converter")
        self.setGeometry(100, 100, 400, 300)
        
        # Main widget and layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)
        
        # Units dictionary
        self.units = {
            'Length': ['meters', 'kilometers', 'centimeters', 'millimeters', 'miles', 'feet', 'inches', 'yards'],
            'Weight': ['kilograms', 'grams', 'milligrams', 'metric tons', 'pounds', 'ounces'],
            'Temperature': ['celsius', 'fahrenheit', 'kelvin', 'rankine'],
            'Volume': ['liters', 'milliliters', 'gallons', 'cubic meters']
        }
        
        # Category dropdown
        self.category_label = QLabel("Category:")
        self.layout.addWidget(self.category_label)
        self.category_combo = QComboBox()
        self.category_combo.addItems(self.units.keys())
        self.layout.addWidget(self.category_combo)
        
        # Value input
        self.value_label = QLabel("Value:")
        self.layout.addWidget(self.value_label)
        self.value_input = QLineEdit()
        self.value_input.setPlaceholderText("Enter value")
        self.layout.addWidget(self.value_input)
        
        # From and To unit dropdowns
        self.from_unit_label = QLabel("From:")
        self.layout.addWidget(self.from_unit_label)
        self.from_unit_combo = QComboBox()
        self.layout.addWidget(self.from_unit_combo)
        
        self.to_unit_label = QLabel("To:")
        self.layout.addWidget(self.to_unit_label)
        self.to_unit_combo = QComboBox()
        self.layout.addWidget(self.to_unit_combo)
        
        # Convert button
        self.convert_button = QPushButton("Convert")
        self.layout.addWidget(self.convert_button)
        
        # Result and error labels
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.result_label)
        
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.error_label)
        
        # Spacer to push content up
        self.layout.addStretch()
        
        # Connect signals
        self.category_combo.currentTextChanged.connect(self.update_units)
        self.convert_button.clicked.connect(self.convert)
        
        # Initialize units
        self.update_units()
    
    def update_units(self):
        category = self.category_combo.currentText()
        self.from_unit_combo.clear()
        self.to_unit_combo.clear()
        self.from_unit_combo.addItems(self.units[category])
        self.to_unit_combo.addItems(self.units[category])
        self.to_unit_combo.setCurrentIndex(1 if len(self.units[category]) > 1 else 0)
        self.result_label.setText("")
        self.error_label.setText("")
    
    def convert(self):
        self.error_label.setText("")
        self.result_label.setText("")
        
        try:
            value = float(self.value_input.text())
            category = self.category_combo.currentText()
            from_unit = self.from_unit_combo.currentText()
            to_unit = self.to_unit_combo.currentText()
            
            if category == 'Length':
                result = self.convert_length(value, from_unit, to_unit)
            elif category == 'Weight':
                result = self.convert_weight(value, from_unit, to_unit)
            elif category == 'Temperature':
                result = self.convert_temperature(value, from_unit, to_unit)
            elif category == 'Volume':
                result = self.convert_volume(value, from_unit, to_unit)
            
            if result is None:
                self.error_label.setText("Invalid unit conversion.")
            else:
                self.result_label.setText(f"Result: {result} {to_unit.capitalize()}")
                
        except ValueError:
            self.error_label.setText("Please enter a valid number.")
    
    def convert_length(self, value, from_unit, to_unit):
        length_units = {
            'meters': 1.0,
            'kilometers': 1000.0,
            'centimeters': 0.01,
            'millimeters': 0.001,
            'miles': 1609.34,
            'feet': 0.3048,
            'inches': 0.0254,
            'yards': 0.9144
        }
        if from_unit not in length_units or to_unit not in length_units:
            return None
        result = value * length_units[from_unit] / length_units[to_unit]
        return round(result, 4)
    
    def convert_weight(self, value, from_unit, to_unit):
        weight_units = {
            'kilograms': 1.0,
            'grams': 0.001,
            'milligrams': 0.000001,
            'metric tons': 1000.0,
            'pounds': 0.453592,
            'ounces': 0.0283495
        }
        if from_unit not in weight_units or to_unit not in weight_units:
            return None
        result = value * weight_units[from_unit] / weight_units[to_unit]
        return round(result, 4)
    
    def convert_temperature(self, value, from_unit, to_unit):
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
    
    def convert_volume(self, value, from_unit, to_unit):
        volume_units = {
            'liters': 1.0,
            'milliliters': 0.001,
            'gallons': 3.78541,
            'cubic meters': 1000.0
        }
        if from_unit not in volume_units or to_unit not in volume_units:
            return None
        result = value * volume_units[from_unit] / volume_units[to_unit]
        return round(result, 4)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UnitConverterApp()
    window.show()
    sys.exit(app.exec_())