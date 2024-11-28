import requests
import re
import json
import argparse
import sys
from urllib.parse import urlparse
import json
import random

def get_user_agent():
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    try:
        with open('user_agents.json') as f:
            d = json.load(f)
            return random.choice(d)
    except:
        print("Using default Chrome User Agent (hardcoded).")
        return ua

# Requests Headers
headers = {
    'User-Agent': get_user_agent(),
}

# Regex to match each marker block
marker_regex = r"var\s*marker[0-9]+\s*=\s*L\.marker\(\[(?P<lat>[0-9|\.]+),\s*(?P<lon>[0-9|\.]+)\],\s*.{2,30}\.bindPopup\('(?P<popupContent>.*?)'\);"

# Function to determine the status based on the popup content
def determine_status(popup_content):
    if 'semistationär' in popup_content:
        return 'semistationary'
    elif 'stationär' in popup_content:
        return 'stationary'
    return 'uncategorized'

# Function to extract the name from the popup content (from the first <span> tag)
def extract_name(popup_content):
    match = re.search(r'<span[^>]*>([^<]*)</span>', popup_content)
    return match.group(1).strip() if match else 'Unknown'

# Function to parse markers
def parse_markers(html_content):
    markers_data = []
    for match in re.finditer(marker_regex, html_content, re.DOTALL):
        latitude = float(match.group('lat'))
        longitude = float(match.group('lon'))
        popup_content = match.group('popupContent')
        
        name = extract_name(popup_content)
        status = determine_status(popup_content)
        
        # Assemble the marker data
        marker_data = {
            'latitude': latitude,
            'longitude': longitude,
            'name': name,
            'status': status
        }
        
        markers_data.append(marker_data)
    
    return markers_data

def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        prog="SPEEED",
        description="Get speed",
    )
    parser.add_argument('url')
    parser.add_argument('-o', '--output-file')
    args = parser.parse_args(argv)

    url = urlparse(str(args.url))
    filename = "locations.json" if not args.output_file else str(args.output_file) 

    # Check url for validity
    if url.scheme == '' or url.netloc == '':
        print("Please add a valid url")
        exit(1)

    # Download the HTML content
    print("Downloading using user-agent: " + headers['User-Agent'])
    response = requests.get(url.geturl(), headers=headers)
    html_content = response.text

    # Parse the markers
    markers_data = parse_markers(html_content)

    # Output the results to "locations.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(markers_data, f, ensure_ascii=False, indent=2)

    print('Parsed markers data saved to ' + filename)

if __name__ == '__main__':
    main()
