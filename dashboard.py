import pandas as pd
import streamlit as st
from datetime import datetime
import requests
import pandas as pd
import logging

def fetch_version_data():
        
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Define the variables to be iterated over
    services = ['stadium', 'canopy', 'loyalty', 'user', 'portico', 'stubs', 'paulie']
    #environments = ['dev', 'qa', 'uat', 'prd']
    environments = ['prd']
    ecosystems = ['ara']
    apps = ['menu', 'refund', 'status', 'loyalty', 'datanow', 'access', 'suites', 'devices']

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
                # if environment in ['dev', 'qa', 'uat'] and ecosystem != 'mars':
                #     continue

                # # Skip prd.mars combination
                # if environment == 'prd' and ecosystem == 'mars':
                #     continue
                
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
    
    for app in apps:
        for environment in environments:
            for ecosystem in ecosystems:
                # Dev, QA, and UAT version checks should only happen in the 'mars' ecosystem
                # if environment in ['dev', 'qa', 'uat'] and ecosystem != 'mars':
                #     continue

                # # Skip prd.mars combination
                # if environment == 'prd' and ecosystem == 'mars':
                #     continue
                
                # Build the URL
                url = f"https://example-{app}.ordernext.com/version.txt"
                
                # Log the URL being accessed
                logging.info(f"Accessing URL: {url}")
                
                # Fetch the txt data from the URL. Each line is a different variable
                try:
                    response = requests.get(url, headers=headers)
                    response_txt = response.text
                    response_txt = response_txt.splitlines()
                    version = response_txt[0]
                    build_date = response_txt[3]
                    
                    # Append to data
                    data.append({
                        'service': app,
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

                
    # Convert data to a pandas DataFrame
    df = pd.DataFrame(data)
    return df

def main():
    st.title('Service Version Dashboard')

    # Fetch the version data
    df = fetch_version_data()

    # Group data by ecosystem and environment
    ecosystems = df['ecosystem'].unique()

    for ecosystem in ecosystems:
        # Filter data for the current ecosystem
        ecosystem_data = df[df['ecosystem'] == ecosystem]

        # Group data by environment within the ecosystem
        environments = ecosystem_data['environment'].unique()

        # Display the ecosystem name as a header
        st.header(ecosystem)

        # Display the tables for each environment within the ecosystem
        for environment in environments:
            # Filter data for the current environment
            environment_data = ecosystem_data[ecosystem_data['environment'] == environment]

            # Display the environment name as a subheader
            st.subheader(environment)

            # Display the table for the environment
            environment_data_display = environment_data[['service', 'version']]
            st.table(environment_data_display.reset_index(drop=True))


if __name__ == '__main__':
    main()