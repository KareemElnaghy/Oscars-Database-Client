import requests
from bs4 import BeautifulSoup
import csv
import re

# Fetch the Wikipedia page
url = "https://en.wikipedia.org/wiki/Academy_Award_for_Best_Actor"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Prepare data storage
data = []  # Main data list
PeopleLinks = set()  # Global set to store unique actor links

# Find all wikitable tables on the page
tables = soup.find_all('table', class_='wikitable')

current_year = None  # Track current year
current_iteration = None  # Track current iteration

# Iterate through tables
for table in tables:
    rows = table.find_all('tr')[1:]  # Skip header row

    for row in rows:
        cols = row.find_all(['td', 'th'])

        # Handle rows with <th> (release year and iteration)
        if cols[0].name == 'th':  # Year and iteration are in <th>
            year_text = cols[0].get_text(strip=True)
            match_year = re.search(r'(\d{4})', year_text)
            match_iteration = re.search(r'\((\d+(?:st|nd|rd|th))\)', year_text)

            if match_year:
                current_year = int(match_year.group(1))
            if match_iteration:
                current_iteration = match_iteration.group(1)

            # Continue processing this row as it may also contain actor/film info
            cols.pop(0)  # Remove <th> from columns to process remaining <td> tags

        # Skip rows without enough columns to process (e.g., empty rows)
        if len(cols) < 3:  # Ensure there are enough columns for actor and film info
            print(f"Skipping row due to insufficient columns: {row}")
            continue

        # Extract actor's name and link from the first <td>
        actor_cell = cols[0]  # First <td> contains the actor info
        actor_link_tag = actor_cell.find('a')  # Find the <a> tag inside <td>

        if not actor_link_tag:  # If no hyperlink is found, skip this entry
            print(f"Skipping row due to missing actor hyperlink: {row}")
            continue

        actor_name = actor_link_tag.get_text(strip=True)
        actor_link = f"https://en.wikipedia.org{actor_link_tag['href']}"
        PeopleLinks.add(actor_link)  # Add actor link to global set

        # Extract film title from the fourth <td>
        film_cell = cols[2] if len(cols) > 2 else None  # Fourth <td> contains the film info
        film_title_tag = film_cell.find('i') if film_cell else None  # Find the <i> tag inside <td>
        film_title_link_tag = film_title_tag.find('a') if film_title_tag else None

        film_title = (
            film_title_link_tag.get_text(strip=True)
            if film_title_link_tag
            else (film_title_tag.get_text(strip=True) if film_title_tag else None)
        )

        if not film_title:  # Skip if no film title is found
            print(f"Skipping row due to missing film title: {row}")
            continue

        # Check winner status (bold indicates winner)
        is_winner = bool(actor_cell.find('b')) or bool(film_cell.find('b'))
        winner_status = "yes" if is_winner else "no"

        entry_data = {
            'movieTitle': film_title,
            'releaseYear': current_year,
            'categoryName': "Best Actor in a Leading Role",
            'iteration': current_iteration,
            'isWinner': winner_status,
            'actor': {
                'firstName': actor_name.split(" ", 1)[0],
                'lastName': actor_name.split(" ", 1)[1] if " " in actor_name else "",
                'link': actor_link
            }
        }

        data.append(entry_data)

# Save data to CSV files

# CSV 1: firstName, lastName, movieTitle, releaseYear, categoryName, iteration, isWinner
with open('best_actor_full_details.csv', mode='w', encoding='utf-8', newline='') as file1:
    writer1 = csv.writer(file1)
    writer1.writerow(['firstName', 'lastName', 'movieTitle', 'releaseYear',
                      'categoryName', 'iteration', 'isWinner'])
    for entry in data:
        writer1.writerow([
            entry['actor']['firstName'],
            entry['actor']['lastName'],
            entry['movieTitle'],
            entry['releaseYear'],
            entry['categoryName'],
            entry['iteration'],
            entry['isWinner']
        ])

# CSV 2: firstName, lastName, movieTitle, releaseYear
with open('best_actor_basic.csv', mode='w', encoding='utf-8', newline='') as file2:
    writer2 = csv.writer(file2)
    writer2.writerow(['firstName', 'lastName', 'movieTitle', 'releaseYear'])
    for entry in data:
        writer2.writerow([
            entry['actor']['firstName'],
            entry['actor']['lastName'],
            entry['movieTitle'],
            entry['releaseYear']
        ])

print("Scraped data saved to best_actor_full_details.csv and best_actor_basic.csv.")
print(f"Total unique people links collected: {len(PeopleLinks)}")
