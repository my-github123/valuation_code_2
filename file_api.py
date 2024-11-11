from flask import Flask, request, jsonify,render_template,redirect
app = Flask(__name__)
year = {
    '1': 0.85,
    '2': 0.8,
    '3': 0.76,
    '4': 0.75,
    '5': 0.71,
    '6': 0.68,
    '7': 0.65,
    '8': 0.633,
    '9': 0.612,
    '10': 0.587,
    '11': 0.573,
    '12': 0.553
}
insurance = {
    '10': +0.02,
    '7': 0.016,
    '3': 0.012,
    '1': 0.007,
    '0': -0.05
}
owner_number = {
    '1': 1.015,
    '2': 0.95,
    '3': 0.92,
    '4': 0.89,
    '5': 0.8823
}
odometer_reading = {
    '5000': 0.022,
    '10000': 0.015,
    '20000': 0.01,
    '40000': -0.01,
    '70000': -0.025,
    '100000': -0.035,
    '150000': -0.055,
    '200000': -0.07,
    '300000': -0.08
}
city_tier = {
    '1': 0.02,
    '2': 0.01,
    '3': -0.01
}
fuel_type = {
    'Petrol': 0.01,
    'Diesel': -0.005
}
transmission_type = {
    'Manual': 0.005,
    'Automatic': -0.005
}
vehicle_category = {
    'Yes': -0.015,
    'No': 0
}

def get_key_from_range(value, ranges):
    for key, (low, high) in ranges.items():
        if low <= value < high:
            return key
    return None

year_ranges = {
    '1': (0, 2),
    '2': (2, 3),
    '3': (3, 4),
    '4': (4, 5),
    '5': (5, 6),
    '6': (6, 7),
    '7': (7, 8),
    '8': (8, 9),
    '9': (9, 10),
    '10': (10, 11),
    '11': (11, 12),
    '12': (12, float('inf'))
}
insurance_ranges = {
    '10': (10,13),
    '7': (7,10 ),
    '3': (3, 7),
    '1': (1, 3),
    '0': (0, 0.1)
}
odometer_ranges = {
    '5000': (0, 5000),
    '10000':(5000,10000),
    '20000': (10000, 20000),
    '40000': (20000, 40000),
    '70000': (40000, 70000),
    '100000': (70000, 100000),
    '150000': (100000, 150000),
    '200000': (150000, 200000),
    '300000': (200000, float('inf')),
}
@app.route('/',methods=['GET'])
def direct():
    if(request.method=='GET'):
        return redirect('/evaluate')
@app.route('/evaluate', methods=['GET','POST'])
def evaluate_vehicle():
    if(request.method=='GET'):
        return render_template('index.html')
    else:
        data = request.form
        price = int(data['price'])
        age = (data['age'])
        months = (data['months'])
        owners = (data['owners'])
        odo_reading = (data['odo_reading'])
        city = (data['city'])
        fuel = data['fuel']
        transmission =data['transmission']
        category = data['category']
        if(price=='' or age=='' or months=='' or owners=='' or odo_reading=='' or city=='' or fuel=='' or transmission=='' or category==''):
            return "<html><body><h3>Fields cannot be empty</h3></body></html>"
        age_key = get_key_from_range(int(age), year_ranges)
        months_key = get_key_from_range(int(months), insurance_ranges)
        odo_reading_key = get_key_from_range(int(odo_reading), odometer_ranges)
        if not age_key or not months_key or not odo_reading_key:
            return jsonify({'error': 'Invalid input ranges'}), 400
        reduced_value = price * year[age_key] * owner_number[owners]
        reduction_factor = (
            1 +
            insurance[months_key] +
            odometer_reading[odo_reading_key] +
            city_tier[city] +
            fuel_type[fuel] +
            transmission_type[transmission] +
            vehicle_category[category]
        )
        final_value = round(reduced_value * reduction_factor)
        return render_template('result.html',price=price,age=age,months=months,owners=owners,odo_reading=odo_reading,city=city,fuel=fuel,transmission=transmission,category=category,value=final_value)
if(__name__=="__main__"):
    app.run(debug=True,port=8000)
