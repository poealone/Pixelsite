import requests
import json
import time
from pyfiglet import Figlet

# Function to print colored text
def print_color(text, color):
    colors = {
        'pink': '\033[95m',
        'yellow': '\033[93m',
        'white': '\033[0m'
    }
    print(colors[color] + text + colors['white'])

# Function to retrieve website status using the Google Pixel API
def check_website_status(url, api_key):
    endpoint = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=' + url + '&key=' + api_key
    response = requests.get(endpoint)
    data = json.loads(response.text)
    return data

# Function to display the website report
def display_website_report(url, api_key):

    data = check_website_status(url, api_key)

    # ASCII art title
    f = Figlet(font='slant')
    print_color(f.renderText('pixelsite'), 'pink')

    # Alert section
    print_color("ALERTS:", 'yellow')
    if 'lighthouseResult' in data:
        audits = data['lighthouseResult']['audits']
        if 'errors-in-console' in audits:
            error_count = audits['errors-in-console']['numericValue']
            if error_count > 0:
                print_color(" - Errors in console: " + str(error_count), 'yellow')

    # Main report section
    print_color("REPORT:", 'white')
    if 'lighthouseResult' in data:
        categories = data['lighthouseResult']['categories']
        for category_name, category_data in categories.items():
            score = category_data['score'] * 100
            print_color(" - " + category_data['title'] + ": " + str(score) + "%", 'white')

    # Scanning animation
    animation = "|/-\\"
    idx = 0

    # Simulating live feed (refresh every 10 seconds)
    while True:
        time.sleep(10)  # Wait for 10 seconds
        print("\n")  # Add empty line to separate reports

        # Retrieve new data for live feed
        data = check_website_status(url, api_key)

        # Clear previous content
        print('\033[F' * 10)

        # Display ASCII box with information
        print_color("┌──────────────────┐", 'white')
        print_color("│   LIVE FEED      │", 'white')
        print_color("├──────────────────┤", 'white')

        # Display active user count
        if 'analytics' in data:
            active_users = data['analytics']['activeUsers']
            print_color("│ Active Users: {:3d} │".format(active_users), 'white')
            print_color("├──────────────────┤", 'white')

        # Display pages with users
        if 'lighthouseResult' in data:
            audits = data['lighthouseResult']['audits']
            if 'network-requests' in audits:
                requests_data = audits['network-requests']
                if 'details' in requests_data:
                    requests_details = requests_data['details']
                    print_color("│ Pages with Users  │", 'white')
                    for request in requests_details:
                        if 'url' in request:
                            print_color("│ - {:<14} │".format(request['url']), 'white')
                    print_color("└──────────────────┘", 'white')

        # Update scanning animation
        print_color("Scanning " + animation[idx % len(animation)], 'white')
        idx = (idx + 1) % len(animation)

# Prompt the user for API key and website URL
api_key = input("Enter your Google Pixel API key: ")
website_url = input("Enter your website URL: ")

# Usage
display_website_report(website_url, api_key)

# Author's name
print("\nby poealone")

