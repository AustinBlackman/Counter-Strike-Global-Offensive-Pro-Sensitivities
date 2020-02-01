import requests
from bs4 import BeautifulSoup
from csv import writer

# Set urls to scrape
urls = ['https://csgopedia.com/csgo-pro-setups/','https://csgopedia.com/csgo-pro-setups/page/2/']

# Initilize needed variables
playerCounter = 0
totalEDPI = 0.0

with open('csgo_player_data.csv', 'w', newline='') as csv_file:
    # Create a csv writer to write data
    csv_writer = writer(csv_file)
    #Create desired top row
    headers = ['Player', 'DPI', 'Game Sensitivity', 'EDPI']
    csv_writer.writerow(headers)

    for url in urls:

        # Set url to scrape
        response = requests.get(url)

        # Create soup object
        soup = BeautifulSoup(response.text, 'html.parser')

        # Create a list of each CSGO player on the page
        players = soup.find_all(class_='set-item')

        for player in players:
            # Create needed variables
            playerCounter += 1
            skip = False

            # Get player name
            name = player.find(class_='username').get_text()

            # Get player DPI and Game Sensitivity
            dpi = player.find_all(class_='pull-right')[0].get_text()
            gameSens = player.find_all(class_='pull-right')[3].get_text()

            # If there is no value recorded or dpi or gameSens, subtract a player as to not interfere with averageEDPI calculation
            if (dpi == '(no value)' or gameSens == '(no value)'):
                skip = True
                edpi = 'not calculable'
                playerCounter -= 1
            else: 
                pass  

            # Convert data to floats for calculation of EDPI if there is a recorded value
            if (skip != True):
                dpi_float = float(dpi)
                gameSens_float = float(gameSens)
                edpi = dpi_float * gameSens_float
                totalEDPI += edpi
            else:
                pass

            # Write row with player data
            csv_writer.writerow([name, dpi, gameSens, edpi])

    # Calculate average EDPI and write it to the last row
    averageEDPI = totalEDPI / playerCounter
    csv_writer.writerow(['Average EDPI -->', averageEDPI])