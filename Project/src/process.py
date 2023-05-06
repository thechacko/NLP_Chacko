from loguru import logger
from datetime import datetime


TODAY = datetime.today().strftime('%Y%m%d')
logger.add(f'./logs/{TODAY}.log', rotation='1 day', retention='7 days', level='INFO')

logger.info('Starting the process')


# Get response from the url
response = use_the_function_to_fetch_the_response()

# Parse and save raw html from the response

# Get the data from the raw html (create a cache function to store the data and delete after 7 days)

# Process the data retrieved from the raw html

# Check for table: staging.news, if not create it

# Insert the processed data into the table

# Fetch the data and perform NER

# Check for table: staging.ner, if not create it 

# Insert the processed data into the table

# Fetch the data and perform sentiment analysis on the data

# Check for table: staging.sent_analysis, if not create it 

# Insert the processed data into the table

# Check for table: app.news, if not create it 

# Store the data from the staging table to the app table
