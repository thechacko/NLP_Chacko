from loguru import logger
from datetime import datetime


TODAY = datetime.today().strftime('%Y%m%d')

# Function to get response from the url
def function_to_get_response_from_the_url():
    try:
        # Get response from the url
        response = requests.get(url)
        logger.info('Fetched the response from the url')
        return response
    except Exception as e:
        logger.error(f'Error in fetching the response from the url: {e}')
        return None


# Function to parse and save raw html from the response

# Function to get the data from the raw html

