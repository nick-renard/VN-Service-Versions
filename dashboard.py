import pandas as pd
import streamlit as st
import requests
import logging
import time

def fetch_version_data(progress_update):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    ecosystems = ['ara', 'lyra', 'crux', 'ln', 'levis', 'levy']
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
        '-suites': 'Suites App',
        '-devices': 'Devices App'
    }
    total_operations = len(ecosystems) * len(services) + len(apps) + 1  # +1 for the additional app fetch at the end
    current_operation = 0
    data = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for ecosystem in ecosystems:
        for service in services:
            url = f"https://{service}.prd.{ecosystem}.vnops.net/version.json"
            logging.info(f"Accessing URL: {url}")

            try:
                response = requests.get(url, headers=headers)
                response_json = response.json()
                version = response_json.get('version')
                build_date = response_json.get('buildDate')
                
                data.append({
                    'type': 'Service',
                    'ecosystem': ecosystem.upper(),
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
                'ecosystem': 'LYRA',
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
            'ecosystem': 'LEVY',
            'name': "Events Catering (Suites-Levy) POS",
            'version': version,
            'build_date': build,
            'url': url
        })

        logging.info(f"Successfully fetched data from {url}")
    except Exception as e:
        logging.error(f"Failed to fetch data from {url}. Error: {e}")
    
    return pd.DataFrame(data)

def display_services_by_ecosystem(df):
    ecosystems = df['ecosystem'].unique()
    for ecosystem in ecosystems:
        st.header(f"{ecosystem} Services")
        ecosystem_df = df[(df['type'] == 'Service') & (df['ecosystem'] == ecosystem)]
        if not ecosystem_df.empty:
            st.table(ecosystem_df[['name', 'version', 'build_date']].reset_index(drop=True))

def display_apps(df):
    st.header("Apps")
    apps_df = df[df['type'] == 'App']
    if not apps_df.empty:
        st.table(apps_df[['ecosystem', 'name', 'version', 'build_date']].reset_index(drop=True))

def main():
    st.title('Service and App Version Dashboard')

    # Initialize the progress bar
    latest_iteration = st.empty()
    bar = st.progress(0)

    def progress_update(current, total):
        progress = int((current / total) * 100)
        latest_iteration.text(f'Fetching data... {progress}%')
        bar.progress(progress)

    df = fetch_version_data(progress_update)

    # Finalize the progress bar
    latest_iteration.text('Fetching data... done!')
    bar.progress(100)
    time.sleep(1)  # Optional: Pause to show completion before moving on

    # Clear the progress display
    latest_iteration.empty()
    bar.empty()

    display_services_by_ecosystem(df)
    display_apps(df)

if __name__ == '__main__':
    main()