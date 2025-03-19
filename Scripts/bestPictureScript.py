import requests
from bs4 import BeautifulSoup
import csv
import re

# Fetch the Wikipedia page
url = "https://en.wikipedia.org/wiki/Academy_Award_for_Best_Picture"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Prepare data storage
data = []  # Main data list
PeopleLinks = set()  # Global set to store unique producer links

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

            # Continue processing this row as it may also contain movie/producers info
            cols.pop(0)  # Remove <th> from columns to process remaining <td> tags

        # Skip rows without enough columns to process (e.g., empty rows)
        if len(cols) < 2:
            print(f"Skipping row due to insufficient columns: {row}")
            continue

        # Extract film title from the <i> tag within the first <td>
        film_cell = cols[0]  # First <td> contains the movie title
        film_title_tag = film_cell.find('i')  # Find the <i> tag inside <td>
        if not film_title_tag:
            print(f"Skipping row due to missing <i> tag")
            continue

        film_title_link_tag = film_title_tag.find('a')  # Check for nested <a> tag

        movie_title = (
            film_title_link_tag.get_text(strip=True)
            if film_title_link_tag
            else film_title_tag.get_text(strip=True)
        )

        # Check winner status (bold indicates winner)
        is_winner = bool(film_cell.find('b'))
        winner_status = "yes" if is_winner else "no"

        # Extract producers from <small> tag in the second <td>
        producers_info = []
        producer_cell = cols[1]  # Second <td> contains producer info
        small_tag = producer_cell.find('small')

        if small_tag:
            producer_links = small_tag.find_all('a')  # Find all <a> tags inside <small>

            if producer_links:  # Case: Hyperlinked producer names
                for link in producer_links:
                    producer_name = link.get_text(strip=True)  # Extract producer name
                    producer_url = f"https://en.wikipedia.org{link['href']}"  # Construct full Wikipedia URL

                    producers_info.append({
                        'producerName': producer_name,
                        'producerLink': producer_url
                    })
                    PeopleLinks.add(producer_url)  # Add to global set of unique links
            else:  # Case: Non-hyperlinked producer names
                plain_producer_names = small_tag.get_text(strip=True).replace("(", "").replace(")", "")
                producers_info.append({
                    'producerName': plain_producer_names,
                    'producerLink': None
                })

        else:  # Case: No producer information present, ignore entry
            continue

        entry_data = {
            'movieTitle': movie_title,
            'releaseYear': current_year,
            'categoryName': "Best Picture",
            'iteration': current_iteration,
            'isWinner': winner_status,
            'producers': producers_info
        }

        data.append(entry_data)

# Save data to CSV files

# CSV 1: firstName, lastName, movieTitle, releaseYear, categoryName, iteration, isWinner
with open('oscar_full_details.csv', mode='w', encoding='utf-8', newline='') as file1:
    writer1 = csv.writer(file1)
    writer1.writerow(['firstName', 'lastName', 'movieTitle', 'releaseYear',
                      'categoryName', 'iteration', 'isWinner'])
    for entry in data:
        for producer in entry['producers']:
            full_name = producer['producerName']
            name_parts = full_name.split(" ", 1) if " " in full_name else [full_name, ""]
            first_name, last_name = name_parts[0], name_parts[1]
            writer1.writerow([
                first_name,
                last_name,
                entry['movieTitle'],
                entry['releaseYear'],
                entry['categoryName'],
                entry['iteration'],
                entry['isWinner']
            ])

# CSV 2: firstName, lastName, movieTitle, releaseYear
with open('oscar_producers_basic.csv', mode='w', encoding='utf-8', newline='') as file2:
    writer2 = csv.writer(file2)
    writer2.writerow(['firstName', 'lastName', 'movieTitle', 'releaseYear'])
    for entry in data:
        for producer in entry['producers']:
            full_name = producer['producerName']
            name_parts = full_name.split(" ", 1) if " " in full_name else [full_name, ""]
            first_name, last_name = name_parts[0], name_parts[1]
            writer2.writerow([
                first_name,
                last_name,
                entry['movieTitle'],
                entry['releaseYear']
            ])

print("Scraped data saved to two CSV files.")
