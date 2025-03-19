import requests
from bs4 import BeautifulSoup
import csv
import re

# Fetch the Wikipedia page
url = "https://en.wikipedia.org/wiki/Academy_Award_for_Best_Director"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Prepare data storage
data = []  # Main data list
PeopleLinks = set()  # Global set to store unique director links

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

            # Continue processing this row as it may also contain director/film info
            cols.pop(0)  # Remove <th> from columns to process remaining <td> tags

        # Skip rows without enough columns to process (e.g., empty rows)
        if len(cols) < 2:
            print(f"Skipping row due to insufficient columns: {row}")
            continue

        # Extract director's name and link from the first <td>
        director_cell = cols[0]  # First <td> contains the director info
        director_link_tag = director_cell.find('a')  # Find the <a> tag inside <td>

        if not director_link_tag:  # If no hyperlink is found, skip this entry
            print(f"Skipping row due to missing director hyperlink: {row}")
            continue

        director_name = director_link_tag.get_text(strip=True)
        director_link = f"https://en.wikipedia.org{director_link_tag['href']}"
        PeopleLinks.add(director_link)  # Add director link to global set

        # Extract film title from the second <td>
        film_cell = cols[1]  # Second <td> contains the film info
        film_title_tag = film_cell.find('i')  # Find the <i> tag inside <td>
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
        is_winner = bool(director_cell.find('b')) or bool(film_cell.find('b'))
        winner_status = "yes" if is_winner else "no"

        entry_data = {
            'movieTitle': film_title,
            'releaseYear': current_year,
            'categoryName': "Best Directing",
            'iteration': current_iteration,
            'isWinner': winner_status,
            'director': {
                'firstName': director_name.split(" ", 1)[0],
                'lastName': director_name.split(" ", 1)[1] if " " in director_name else "",
                'link': director_link
            }
        }

        data.append(entry_data)

# Save data to CSV files

# CSV 1: firstName, lastName, movieTitle, releaseYear, categoryName, iteration, isWinner
with open('best_directing_full_details.csv', mode='w', encoding='utf-8', newline='') as file1:
    writer1 = csv.writer(file1)
    writer1.writerow(['firstName', 'lastName', 'movieTitle', 'releaseYear',
                      'categoryName', 'iteration', 'isWinner'])
    for entry in data:
        writer1.writerow([
            entry['director']['firstName'],
            entry['director']['lastName'],
            entry['movieTitle'],
            entry['releaseYear'],
            entry['categoryName'],
            entry['iteration'],
            entry['isWinner']
        ])

# Write CSV 2: basic details
with open('best_directing_basic.csv', mode='w', encoding='utf-8', newline='') as file2:
    writer2 = csv.writer(file2)
    writer2.writerow(['firstName', 'lastName', 'movieTitle', 'releaseYear'])
    for entry in data:
        writer2.writerow([
            entry['director']['firstName'],
            entry['director']['lastName'],
            entry['movieTitle'],
            entry['releaseYear'],
        ])

print("Scraped data saved to best_directing_full_details.csv and best_directing_basic.csv.")
print(f"Total unique people links collected: {len(PeopleLinks)}")

