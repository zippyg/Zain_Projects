from flask import Flask, render_template, request, redirect, url_for, flash
import os
import secrets

# Generate a random secret key
app.secret_key = secrets.token_hex(16)  # Generates a secure token with 16 bytes of randomness, encoded in hexadecimal

app = Flask(__name__)
#app.secret_key = 'your_secret_key'  # Necessary for session management and flash messages

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            # Extract and convert all inputs from the form
            bedroom_lengths = [float(request.form[f'length{i}']) for i in range(1, 4)]
            bedroom_widths = [float(request.form[f'width{i}']) for i in range(1, 4)]
            total_floor_area = float(request.form['total_floor_area'])
            monthly_rent = float(request.form['monthly_rent'])

            # Calculate areas and rents
            bedroom_areas = [l * w for l, w in zip(bedroom_lengths, bedroom_widths)]
            total_bedroom_area = sum(bedroom_areas)

            weekly_rents = [
                (((total_floor_area - total_bedroom_area) / total_floor_area) * (monthly_rent / (4.35 * 3)) +
                 (area / total_floor_area) * (monthly_rent / 4.35))
                for area in bedroom_areas
            ]

            # Check if the total weekly rent * 4.35 equals the monthly rent
            if abs(sum(weekly_rents) * 4.35 - monthly_rent) < 0.01:
                return render_template('result.html', weekly_rents=weekly_rents)
            else:
                flash("The total weekly rent times 4.35 does not match the monthly rent. Please check your inputs.")
                return redirect(url_for('home'))

        except ValueError:
            flash("Please enter valid numerical values.")
            return redirect(url_for('home'))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
