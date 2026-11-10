from flask import Flask, render_template

# Initialize the Flask application
app = Flask(__name__)


# Define the homepage route
@app.route('/')
def home():
  # We can pass variables from Python directly into our HTML page!
  app_title = 'Kenyan Transport Tariff Calculator'
  base_fare = 150  # KES
  return render_template(
      'index.html', title=app_title, fare=base_fare
  )


if __name__ == '__main__':
  # Run the local server in debug mode
  app.run(debug=True, port=5000)
