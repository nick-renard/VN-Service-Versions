import os
from datetime import datetime
import requests
import pandas as pd
import time
import logging
from openpyxl import Workbook

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the variables to be iterated over
services = ['stadium', 'canopy', 'loyalty', 'user', 'portico', 'stubs', 'paulie']
environments = ['dev', 'qa', 'uat', 'prd']
ecosystems = ['ara', 'lyra', 'levy', 'crux', 'levis', 'draco', 'mars']

# Data to be written to excel
data = []

# User-Agent string to mimic a web browser, otherwise SSL handshake fails
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Iterate over each combination of SERVICE, ENVIRONMENT, and ECOSYSTEM, but skip prd.mars iterations
for service in services:
    for environment in environments:
        for ecosystem in ecosystems:
            # Dev, QA, and UAT version checks should only happen in the 'mars' ecosystem
            if environment in ['dev', 'qa', 'uat'] and ecosystem != 'mars':
                continue

            # Skip prd.mars combination
            if environment == 'prd' and ecosystem == 'mars':
                continue
            
            # Build the URL
            url = f"https://{service}.{environment}.{ecosystem}.vnops.net/version.json"
            
            # Log the URL being accessed
            logging.info(f"Accessing URL: {url}")

            # Fetch the JSON data from the URL
            try:
                response = requests.get(url, headers=headers)
                response_json = response.json()
                
                # Extract version and buildDate
                version = response_json.get('version')
                build_date = response_json.get('buildDate')
                
                # Append to data
                data.append({
                    'service': service,
                    'environment': environment,
                    'ecosystem': ecosystem,
                    'version': version,
                    'build_date': build_date,
                    'url': url
                })

                # Log success
                #logging.info(f"Successfully fetched data from {url}")
                logging.info('\x1b[0;30;42m' + f"Successfully fetched data from {url}" + '\x1b[0m')
                #print('\x1b[0;30;42m' + f"Successfully fetched data from {url}" + '\x1b[0m')
            except Exception as e:
                # Log error
                logging.error(f"Failed to fetch data from {url}. Error: {e}")

            # Pause for 2 seconds to prevent overloading, is this even necessary? prolly not
            #time.sleep(2)

# Convert data to a pandas DataFrame
df = pd.DataFrame(data)

# Get the current date and time
current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

# Define the path
filename = f'version_data_{current_datetime}.xlsx'

output_path = 'GET_SERVICE_VERSIONS/Outputs/' + filename

# Write DataFrame to Excel
df.to_excel(output_path, index=False, sheet_name='Version Data')

# Log final message
logging.info(f"Data saved to '{output_path}'")
