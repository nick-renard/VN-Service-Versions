import pandas as pd
import streamlit as st
import requests
import logging

def fetch_version_data():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    #ecosystems = ['ara', 'lyra', 'levy', 'crux', 'ln', 'levis', 'draco']
    services = ['stadium', 'canopy', 'loyalty', 'user', 'portico', 'stubs', 'paulie', 'moneyball']
    apps = ['-pos', 'fs-pos', 'ec-pos', '', '-menu', '-refund', '-status', '-loyalty', '-datanow', '-access', '-suites', '-devices']
    app_names = {
        '-pos': 'Quick Service POS',
        'fs-pos': 'Full Service POS',
        'ec-pos': 'Events Catering (Suites-Levy) POS',
        '-menu': 'Menu Manager',
        '': 'Mobile Ordering',
        '-refund': 'Orders App',
        '-status': 'Status App',
        '-loyalty': 'Loyalty App',
        '-datanow': 'DataNow',
        '-access': 'Access App',
        '-suites': 'Suite App',
        '-devices': 'Device App'
    }
    data = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for service in services:
        url = f"https://{service}.prd.lyra.vnops.net/version.json"
        logging.info(f"Accessing URL: {url}")

        try:
            response = requests.get(url, headers=headers)
            response_json = response.json()
            version = response_json.get('version')
            build_date = response_json.get('buildDate')
            
            data.append({
                'type': 'Service',
                'name': service.capitalize(),
                'version': version,
                'build_date': build_date,
                'url': url
            })

            logging.info(f"Successfully fetched data from {url}")
        except Exception as e:
            logging.error(f"Failed to fetch data from {url}. Error: {e}")

    for app_code in apps:
        app_name = app_names.get(app_code, "Unknown App")
        url = f"https://validationssandbox{app_code}.ordernext.com/version.txt"
        logging.info(f"Accessing URL: {url}")
        
        try:
            response = requests.get(url, headers=headers)
            response_txt = response.text.splitlines()
            version_line = response_txt[0]
            # Extract the version number after "="
            version = version_line.split('=')[1] if '=' in version_line else version_line
            build_date = response_txt[3]
            build = build_date.split('=')[1] if '=' in build_date else build_date
            
            data.append({
                'type': 'App',
                'name': app_name,
                'version': version,
                'build_date': build,
                'url': url
            })

            logging.info(f"Successfully fetched data from {url}")
        except Exception as e:
            logging.error(f"Failed to fetch data from {url}. Error: {e}")
            
    url = f"https://elevy-pos.ordernext.com/version.txt"
    logging.info(f"Accessing URL: {url}")
    
    try:
        response = requests.get(url, headers=headers)
        response_txt = response.text.splitlines()
        version_line = response_txt[0]
        # Extract the version number after "="
        version = version_line.split('=')[1] if '=' in version_line else version_line
        build_date = response_txt[3]
        build = build_date.split('=')[1] if '=' in build_date else build_date
        
        data.append({
            'type': 'App',
            'name': app_name,
            'version': version,
            'build_date': build,
            'url': url
        })

        logging.info(f"Successfully fetched data from {url}")
    except Exception as e:
        logging.error(f"Failed to fetch data from {url}. Error: {e}")
    
    return pd.DataFrame(data)

def display_data(df, data_type):
    st.header(f"{data_type}s")
    filtered_df = df[df['type'] == data_type]
    if not filtered_df.empty:
        st.table(filtered_df[['name', 'version', 'build_date']].reset_index(drop=True))

def main():
    st.title('Service and App Version Dashboard [LYRA Versions]')
    df = fetch_version_data()

    display_data(df, 'Service')
    display_data(df, 'App')
    
if __name__ == '__main__':
    main()
