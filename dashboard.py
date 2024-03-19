import pandas as pd
import streamlit as st
import requests
import logging

def fetch_version_data():
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    services = ['stadium', 'canopy', 'loyalty', 'user', 'portico', 'stubs', 'paulie']
    environments = ['prd']
    ecosystems = ['ara']
    apps = ['-pos', '', '-menu', '-refund', '-status', '-loyalty', '-datanow', '-access', '-suites', '-devices']
    data = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for service in services:
        for environment in environments:
            for ecosystem in ecosystems:
                url = f"https://{service}.prd.{ecosystem}.vnops.net/version.json"
                logging.info(f"Accessing URL: {url}")

                try:
                    response = requests.get(url, headers=headers)
                    response_json = response.json()
                    version = response_json.get('version')
                    build_date = response_json.get('buildDate')
                    
                    data.append({
                        'type': 'service',
                        'name': service,
                        'version': version,
                        'build_date': build_date,
                        'url': url
                    })

                    logging.info(f"Successfully fetched data from {url}")
                except Exception as e:
                    logging.error(f"Failed to fetch data from {url}. Error: {e}")

    for app in apps:
        url = f"https://example{app}.ordernext.com/version.txt"
        logging.info(f"Accessing URL: {url}")
        
        try:
            response = requests.get(url, headers=headers)
            response_txt = response.text.splitlines()
            version = response_txt[0]
            build_date = response_txt[3]
            
            data.append({
                'type': 'app',
                'name': app,
                'version': version,
                'build_date': build_date,
                'url': url
            })

            logging.info(f"Successfully fetched data from {url}")
        except Exception as e:
            logging.error(f"Failed to fetch data from {url}. Error: {e}")
    
    return pd.DataFrame(data)

def display_data(df, data_type):
    st.header(f"{data_type.capitalize()}s")
    unique_names = df['name'].unique()

    for name in unique_names:
        name_data = df[df['name'] == name]
        st.subheader(name)
        st.table(name_data[['name', 'version']].reset_index(drop=True))

def main():
    st.title('Service and App Version Dashboard')
    df = fetch_version_data()

    # Separate data into services and apps
    services_df = df[df['type'] == 'service']
    apps_df = df[df['type'] == 'app']

    if not services_df.empty:
        display_data(services_df, 'service')
    
    if not apps_df.empty:
        display_data(apps_df, 'app')
    
if __name__ == '__main__':
    main()
