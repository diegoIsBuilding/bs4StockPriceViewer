from bs4 import BeautifulSoup
import requests
import random
import os
import json 

#Make sure the directories for raw/processed data exist
if not os.path.exists('data/raw'):
    os.makedirs('data/raw')
if not os.path.exists('data/processed'):
    os.makedirs('data/processed')
    
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
            session.headers.update(headers)
            response = session.get(url, verify=False, timeout=10)
        response.raise_for_status()
        
        
        
        
        
    #Works with the try block
    except requests.ConnectionError:
        print('Failed to connect to website')
    except requests.Timeout:
        print('The request timed out')
    except requests.RequestException as e:
        print(f'An error occurred while fetching the data: {e}')
    except Exception as e:
        print(f'An unexpected error occurred: {e}')