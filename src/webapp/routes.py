from flask import render_template
import sys
import os
from . import app

# Get the absolute path of the src directory
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, '..', '..')

# Add the src directory to sys.path
sys.path.append(src_dir)

# Now you can import your module
from src.analysis.plotter import plot_stock_data, load_stock_data_from_json

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plot')
def plot():
    stock_data = load_stock_data_from_json()
    data_plot = plot_stock_data(stock_data)
    
    return render_template('plot.html', data_plot=data_plot)
