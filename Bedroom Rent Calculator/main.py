from flask import Flask, render_template, request, flash, redirect, url_for
import os
from decimal import Decimal, getcontext

# Set decimal precision to a high value for accuracy
getcontext().prec = 28

app = Flask(__name__, template_folder='.')
# Set a secret key for session management and flash messages
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'a_default_secret_key_for_dev')

@app.route('/', methods=['GET', 'POST'])
def welcome():
    if request.method == 'POST':
        try:
            num_bedrooms = int(request.form['num_bedrooms'])
            return redirect(url_for('home', num_bedrooms=num_bedrooms))
        except ValueError:
            flash("Please enter a valid number of bedrooms.")
            return redirect(url_for('welcome'))
    return render_template('welcome.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    num_bedrooms = int(request.args.get('num_bedrooms', 1))
    if request.method == 'POST':
        try:
            # Extract form data and convert to Decimal for precise calculation
            bedroom_lengths = [Decimal(request.form[f'length{i}']) for i in range(1, num_bedrooms + 1)]
            bedroom_widths = [Decimal(request.form[f'width{i}']) for i in range(1, num_bedrooms + 1)]
            total_floor_area = Decimal(request.form['total_floor_area'])
            monthly_rent = Decimal(request.form['monthly_rent'])

            # Calculate areas and weekly rents
            bedroom_areas = [length * width for length, width in zip(bedroom_lengths, bedroom_widths)]
            total_bedroom_area = sum(bedroom_areas)
            weekly_rents = [
                (((total_floor_area - total_bedroom_area) / total_floor_area) * (monthly_rent / (Decimal('4.35') * num_bedrooms)) +
                 (area / total_floor_area) * (monthly_rent / Decimal('4.35')))
                for area in bedroom_areas
            ]

            # Validate if the total weekly rents are correct
            if abs(sum(weekly_rents) * Decimal('4.35') - monthly_rent) < Decimal('0.01'):
                # Render result template with weekly rents
                return render_template('result.html', weekly_rents=weekly_rents)
            else:
                flash("The total weekly rent times 4.35 does not match the monthly rent. Please check your inputs.")
                return redirect(url_for('home', num_bedrooms=num_bedrooms))
        except Exception as e:
            flash(f"Error: {str(e)}")
            return redirect(url_for('home', num_bedrooms=num_bedrooms))

    return render_template('index.html', num_bedrooms=num_bedrooms)

if __name__ == '__main__':
    app.run(debug=True)  # Set debug=False in production environment
