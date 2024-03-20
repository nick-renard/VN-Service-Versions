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

    # Calculating total operations more accurately
    total_operations = (len(ecosystems) * len(services)) + len(apps) + 1  # Assuming +1 for the extra fetch at the end
    current_operation = 0

    data = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for ecosystem in ecosystems:
        for service in services:
            url = f"https://{service}.prd.{ecosystem}.vnops.net/version.json"
            try:
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
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
            except Exception as e:
                logging.error(f"Failed to fetch data from {url}. Error: {e}")
            finally:
                current_operation += 1
                progress_update(current_operation / total_operations * 100)

    for app_code in apps:
        app_name = app_names.get(app_code, "Unknown App")
        url = f"https://validationssandbox{app_code}.ordernext.com/version.txt"
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                response_txt = response.text.splitlines()
                version_line = response_txt[0]
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
        except Exception as e:
            logging.error(f"Failed to fetch data from {url}. Error: {e}")
        finally:
            current_operation += 1
            progress_update(current_operation / total_operations * 100)
    
    return pd.DataFrame(data)

def main():
    st.title('Service and App Version Dashboard')
    progress_text = "Fetching data... please wait..."
    progress_bar = st.progress(0, text=progress_text)

    def progress_update(progress):
        progress_bar.progress(int(progress))

    df = fetch_version_data(progress_update)

    # Displaying the data
    if not df.empty:
        services_df = df[df['type'] == 'Service']
        if not services_df.empty:
            st.header("Services")
            st.dataframe(services_df[['ecosystem', 'name', 'version', 'build_date']].reset_index(drop=True))
            apps_df = df[df['type'] == 'App']
            
    if not apps_df.empty:
        st.header("Apps")
        st.dataframe(apps_df[['ecosystem', 'name', 'version', 'build_date']].reset_index(drop=True))

st.button("Rerun")

if __name__ == '__main__':
    main()