import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import os
import json

def load_stock_data_from_json():
    #Get the directory of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))
    
    #Construct the full path to the JSON file
    json_path = os.path.join(current_directory, '..', '..', 'data', 'processed', 'apple_stock_data.json')
    
    with open(json_path, 'r') as file:
        stock_data = json.load(file)
    return stock_data

def plot_stock_data(stock_data):
    #Get the current directory of the plotter.py file
    current_directory = os.path.dirname(os.path.abspath(__file__))
    
    #Construct the path to the img directory
    img_dir_path = os.path.join(current_directory, '..', 'webapp', 'static', 'img')
    
    #Convert the list of dictionaries to a DataFrame
    df_Conversion = pd.DataFrame(stock_data)
    
    #Convert the 'date' column to datetime format
    df_Conversion['date'] = pd.to_datetime(df_Conversion['date'])
    
    #Sort the data by date
    df_Conversion = df_Conversion.sort_values('date')
    
    # Convert the 'price' column to float
    df_Conversion['price'] = df_Conversion['price'].astype(float)
    
    # Calculate the daily fluctuation compared to the previous day
    df_Conversion['daily_fluctuation'] = df_Conversion['price'].diff()
    
    # Instead of adjusting the first row, just set NaN to 0
    df_Conversion['daily_fluctuation'].fillna(0, inplace=True)
    
    # Create the adjusted price series
    df_Conversion['adjusted_price'] = df_Conversion['price'].iloc[0] + df_Conversion['daily_fluctuation'].cumsum()
    
    # Plotting
    plt.figure(figsize=(10,6))
    
    # Plot the adjusted price over time
    plt.plot(df_Conversion['date'], df_Conversion['adjusted_price'], marker = 'o', linestyle = '-')
    
    plt.title('Apple Stock Price Fluctuation Over a Month')
    plt.xlabel('Date')
    plt.ylabel('Adjusted Open Price ($)') 
    plt.grid(True)
    plt.tight_layout()
    
    # Save the plot to the static/img directory (will use in web app)
    plot_path = os.path.join(img_dir_path, 'apple_stock_plot.png')
    
    # Ensure the directory exists
    os.makedirs(img_dir_path, exist_ok=True)
    
    plt.savefig(plot_path)
    
    #Display the plot
    #plt.show()
    
    return plot_path #Return the path to the saved plot


