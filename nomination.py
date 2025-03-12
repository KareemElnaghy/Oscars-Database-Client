import requests
from bs4 import BeautifulSoup
import csv
import re

# Fetch the Wikipedia page
url = "https://en.wikipedia.org/wiki/Academy_Award_for_Best_Visual_Effects"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Prepare data storage
data = []

# Find all wikitable tables on the page
tables = soup.find_all('table', class_='wikitable')

current_year = None  # Track current year
current_iteration = None  # Track current iteration

# Iterate through tables
for table in tables:
    if any(th.get_text(strip=True) == 'Finalists' for th in table.find_all('th')):
        break
    rows = table.find_all('tr')[1:]  # Skip header row

    for row in rows:
        cols = row.find_all(['td', 'th'])

        # Check if this row has a valid year
        year_text = cols[0].get_text(strip=True) if len(cols) > 0 else ''
        match_year = re.search(r'(\d{4})', year_text)
        match_iteration = re.search(r'\((\d+(?:st|nd|rd|th))\)', year_text)

        if match_year:
            current_year = int(match_year.group(1))
            if match_iteration:
                current_iteration = match_iteration.group(1)
        elif current_year is None:
            continue
        else:
            # If no new year found, keep using last known year
            pass

        # Extract film title
        if len(cols) > 1:
            # Check if this row is a winner row
            is_winner = bool(cols[1].find('b'))

            if is_winner: winner = "yes"
            else: winner = "no"

            if is_winner:
                film_cell = cols[1].get_text(strip=True).replace('***', '').replace('*', '')
            else:
                # If not a winner row, check if it's a film title row
                if any(keyword in cols[0].get_text(strip=True).lower() for keyword in ["finalists", "first round", "second round"]):
                    continue
                film_cell = cols[0].get_text(strip=True).replace('***', '').replace('*', '')

            clean_film_title = re.sub(r'\[note \d+\]', '', film_cell).strip()

            # Handle multiple films in the same cell
            films = re.split(r',| and ', clean_film_title)
            films = [f.strip() for f in films if f.strip()]

            for film in films:
                # Add to data collection
                data.append({
                    'year': current_year,
                    'film': film,
                    'iteration': current_iteration,
                    'is_winner': winner,
                    'categoryName': "Best Visual Effects"
                })

# Save data to CSV file
with open('oscar_visual_effects.csv', mode='w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['movieTitle', 'releaseDate', 'categoryName', 'iteration', 'isWinner'])

    for entry in data:
        if entry['year'] is not None:  # Ensure valid year entries only
            writer.writerow([
                entry['film'],
                entry['year'],
                entry['categoryName'],
                entry['iteration'],
                entry['is_winner']
            ])

print("Scraped data saved to 'oscar_visual_effects.csv'")
