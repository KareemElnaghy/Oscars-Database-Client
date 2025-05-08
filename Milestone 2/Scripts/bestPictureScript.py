import requests
from bs4 import BeautifulSoup
import csv
import re

url = "https://en.wikipedia.org/wiki/Academy_Award_for_Best_Picture"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

data = []
PeopleLinks = set()

tables = soup.find_all('table', class_='wikitable')

current_year = None
current_iteration = None

for table in tables:
    rows = table.find_all('tr')[1:]

    for row in rows:
        cols = row.find_all(['td', 'th'])

        if cols[0].name == 'th':
            year_text = cols[0].get_text(strip=True)
            match_year = re.search(r'(\d{4})', year_text)
            match_iteration = re.search(r'\((\d+(?:st|nd|rd|th))\)', year_text)

            if match_year:
                current_year = int(match_year.group(1))
            if match_iteration:
                current_iteration = match_iteration.group(1)

            cols.pop(0)

        if len(cols) < 2:
            continue

        film_cell = cols[0]
        film_title_tag = film_cell.find('i')
        if not film_title_tag:
            continue

        film_title_link_tag = film_title_tag.find('a')
        movie_title = (
            film_title_link_tag.get_text(strip=True)
            if film_title_link_tag
            else film_title_tag.get_text(strip=True)
        )

        is_winner = bool(film_cell.find('b'))
        winner_status = "yes" if is_winner else "no"

        producers_info = []
        producer_cell = cols[1]
        small_tag = producer_cell.find('small')

        if small_tag:
            producer_links = small_tag.find_all('a')

            if producer_links:
                for link in producer_links:
                    producer_name = link.get_text(strip=True)
                    producer_url = f"https://en.wikipedia.org{link['href']}"

                    producers_info.append({
                        'producerName': producer_name,
                        'producerLink': producer_url
                    })
                    PeopleLinks.add(producer_url)
            else:
                plain_producer_names = small_tag.get_text(strip=True).replace("(", "").replace(")", "")
                producers_info.append({
                    'producerName': plain_producer_names,
                    'producerLink': None
                })

        else:
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

with open('best_picture.csv', mode='w', encoding='utf-8', newline='') as file1:
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

print("Scraped data saved to two CSV files.")