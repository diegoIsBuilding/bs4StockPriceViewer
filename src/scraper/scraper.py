from bs4 import BeautifulSoup
import requests
import random
import os
import json 

#Make sure the directories for raw/processed data exist
# Get the current script's directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Define the path to the data directories from the current script's location
raw_data_path = os.path.join(current_directory, '..', '..', 'data', 'raw')
processed_data_path = os.path.join(current_directory, '..', '..', 'data', 'processed')

# Create the directories if they don't exist
if not os.path.exists(raw_data_path):
    os.makedirs(raw_data_path)
if not os.path.exists(processed_data_path):
    os.makedirs(processed_data_path)
#Fetch the stock data for Apple
#Retrieve the open price for the last 2 year (10/14/21 - 10/14/23)

#Create a function that scrapes a specific url,
#has a list of user agenst, headers, and referer

def fetch_apple_stock_data():
    url = 'https://www.investing.com/equities/apple-computer-inc-historical-data'
    referer = 'https://www.investing.com'
    #Rotate through different user agents to avoid being blocked
    #User agents just send browser info to web servers
    #Info includes browerser version and operating system
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/117.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    ]
    #The headers dictionary defines HTTP headers that will 
    #be sent WITH the web request
    headers = {
        #Select random user agent from the list above
        'User-Agent': random.choice(user_agents),
        #Indicates the previous web page from which the url
        #is being requested (See the where the traffic is coming from)
        'Referer': referer
    }
    def append_to_stock_data(dates, prices):
        '''Utility function to append article data to article_info list'''
        data = {
            'date': dates,
            'price': prices,
        }
        stock_data.append(data)
    
    #Create a try block
    #The block is used to catch any exceptions that may occur
    #If caught these can be handled
    try:
        #This line initializes a session using requests
        #Sessions: allows you to make multiple requests to 
        #the same website (reuse underlying TCP connection)
        
        #WITH KEYWORD: this makes sure that the session is
        #properly closed after it is done
        with requests.Session() as session:
            #This updates the headers with the headers
            #defined in the 'headers' dictionary
            session.headers.update(headers)
            #This sends a GET request to the url
            #The timeout method specifies that if there
            #is no response in 10 seconds a timeout exception
            #will be raised
            response = session.get(url, timeout=10)
        #If the HTTP request returns an error code like 
        #404 or 500 this will return an HTTPError exception 
        response.raise_for_status()
        
        #'with' makes sure that the file is properly closed
        #after the operations in the block have successfully 
        #been completed
        # Define the full path to the file
        raw_file_path = os.path.join(raw_data_path, 'apple_stock_data.html')
        processed_file_path = os.path.join(processed_data_path, 'apple_stock_data.json')

        # Use the full path in the open function
        with open(raw_file_path, 'w', encoding='utf-8') as file:
            file.write(response.text)
        #Check if the file has automatically been closed
        #file.closed
        
        soup = BeautifulSoup(response.text, 'lxml')
        table_data = soup.find('table', class_ = 'w-full text-xs leading-4 overflow-x-auto freeze-column-w-1')
        open_stock_price_dates_container = table_data.find_all('td', class_ = 'datatable_cell__LJp3C text-left align-middle overflow-hidden text-v2-black text-ellipsis whitespace-nowrap text-sm font-semibold leading-4 min-w-[106px] left-0 sticky bg-white sm:bg-inherit')
        open_stock_prices = table_data.find_all('td', class_ = 'text-v2-black text-right text-sm font-normal leading-5 align-middle min-w-[77px] rtl:text-right')
        
        stock_data = []
        if table_data:
            for date in open_stock_price_dates_container:
                if date:
                    dates = date.find('time').text.strip()
                else: dates = 'Unknown'
            for stock_price in open_stock_prices:
                if stock_price:
                    prices = stock_price.text.strip()
                else: prices = 'Unknown'
                print(dates, prices)
              
        
            
            
            
            
        '''open_price_data = soup.find_all('td', class_ = 'text-v2-black text-right text-sm font-normal leading-5 align-middle min-w-[77px] rtl:text-right')
        stock_date_data = soup.find_all()
        list_of_open_stock_price = []
        for open_stock_prices in open_price_data:
            stock_price = open_stock_prices.text.strip()
            list_of_open_stock_price.append({
                'open': stock_price
            })'''
        
            
        with open(processed_file_path, 'w') as file:
            json.dump(stock_data, file, indent=4)
        
    #Works with the try block
    except requests.ConnectionError:
        print('Failed to connect to website')
    except requests.Timeout:
        print('The request timed out')
    except requests.RequestException as e:
        print(f'An error occurred while fetching the data: {e}')
    except Exception as e:
        print(f'An unexpected error occurred: {e}')

fetch_apple_stock_data()