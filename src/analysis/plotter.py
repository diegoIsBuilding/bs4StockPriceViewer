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
    #Convert the list of dictionaries to a DataFrame
    df_Conversion = pd.DataFrame(stock_data)
    
    #Convert the 'date' column to datetime format
    df_Conversion['date'] = pd.to_datetime(df_Conversion['date'])
    
    #Sort the data by date
    df_Conversion = df_Conversion.sort_values('date')
    
    #Plotting
    plt.figure(figsize=(10,6))
    plt.plot(df_Conversion['date'], df_Conversion['price'], marker = 'o', linestyle = '-')
    plt.title('Apple Stock Price of a Month')
    plt.xlabel('Date')
    plt.ylabel('Open Price')
    plt.grid(True)
    plt.tight_layout()
    
    #Save the plot to the static/img directory (will use in web app)
    plot_path = 'src/webapp/static/img/apple_stock_plot.png'
    plt.savefig(plot_path)
    
    #Display the plot
    plt.show()
    
    return plot_path #Return the path to the saved plot