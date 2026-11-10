from datetime import datetime
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
  # Default output state when the page first loads
  results = None

  if request.method == 'POST':
    try:
      # Retrieve form data submitted by the user
      distance_km = float(request.form.get('distance_km', 0))
      fuel_price = float(request.form.get('fuel_price', 180))  # KES per Liter
      efficiency_kml = float(request.form.get('efficiency_kml', 12))  # km/L
      sacco_base_fare = float(request.form.get('sacco_base_fare', 100))
      days_per_month = int(request.form.get('days_per_month', 22))
      is_peak = 'is_peak' in request.form

      # 1. Fuel Calculation Engine
      liters_needed = distance_km / efficiency_kml if efficiency_kml > 0 else 0
      total_fuel_cost = liters_needed * fuel_price

      # 2. Peak-Hour Matatu Tariff Multiplier
      peak_multiplier = 1.5 if is_peak else 1.0
      single_trip_fare = sacco_base_fare * peak_multiplier
      daily_commute_fare = single_trip_fare * 2  # Round trip

      # 3. Commuter Budget Calculations
      weekly_budget = daily_commute_fare * 5
      monthly_budget = daily_commute_fare * days_per_month

      results = {
          'distance_km': distance_km,
          'fuel_price': fuel_price,
          'liters_needed': round(liters_needed, 2),
          'total_fuel_cost': round(total_fuel_cost, 2),
          'single_trip_fare': round(single_trip_fare, 2),
          'daily_commute_fare': round(daily_commute_fare, 2),
          'weekly_budget': round(weekly_budget, 2),
          'monthly_budget': round(monthly_budget, 2),
          'is_peak': is_peak,
      }
    except ValueError:
      results = {'error': 'Please enter valid numerical values.'}

  return render_template('index.html', results=results)


if __name__ == '__main__':
  app.run(debug=True, port=5000)
