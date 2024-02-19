import requests
import re
import subprocess

def scrape_co2_level(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Extracting CO2 level using regular expression
            co2_data = re.search(r'co2_level_ppm\s+(\d+\.\d+)', response.text)
            if co2_data:
                co2_level = float(co2_data.group(1))
                return int(co2_level)  # Convert to integer
            else:
                print("CO2 level data not found in the response.")
        else:
            print("Failed to fetch data from the URL. Status code:", response.status_code)
    except Exception as e:
        print("An error occurred while scraping data:", str(e))

def send_curl_notification(co2_level):
    try:
        if co2_level > 1500:
            # Replace the username, password and the ntfy url with your own infos
            curl_command = f'curl -u "<username>:<password>" -H "t: High CO₂ value 📈" -d "{co2_level} ppm" https://ntfy.example.com/topic > /dev/null 2>&1'
            subprocess.run(curl_command, shell=True, check=True)
            print("Curl command executed successfully.")
    except Exception as e:
        print("An error occurred while sending curl request:", str(e))

if __name__ == "__main__":
    # Replace the prometheus client url with your own (where the CO2 metrics are exposed)
    prometheus_client_url = "http://<your-prometheus-client-url>:8000"
    co2_level = scrape_co2_level(prometheus_client_url)
    if co2_level:
        print(co2_level)
        send_curl_notification(co2_level)
