import requests
from bs4 import BeautifulSoup
import csv
import re

url = "https://en.wikipedia.org/wiki/List_of_Academy_Award_winners_and_nominees_for_Best_International_Feature_Film"
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

        if cols and cols[0].name == 'th':
            year_text = cols[0].get_text(strip=True)
            match_year = re.search(r'(\d{4})', year_text)
            match_iteration = re.search(r'\((\d+(?:st|nd|rd|th))\)', year_text)

            if match_year:
                current_year = int(match_year.group(1))
            if match_iteration:
                current_iteration = match_iteration.group(1)

            cols.pop(0)

        if len(cols) < 3:
            continue

        directorIndex = 2
        film_cell = cols[0]
        if 'colspan' in film_cell.attrs:
            directorIndex = 1
        film_title_tag = film_cell.find('i')
        if not film_title_tag:
            continue

        film_title_link_tag = film_title_tag.find('a')
        movie_title = (
            film_title_link_tag.get_text(strip=True)
            if film_title_link_tag
            else film_title_tag.get_text(strip=True)
        )

        director_cell = cols[directorIndex]
        director_links_tags = director_cell.find_all('a')

        nominees_info = []
        for link in director_links_tags:
            director_name = link.get_text(strip=True)
            director_url = f"https://en.wikipedia.org{link['href']}"
            PeopleLinks.add(director_url)

            nominees_info.append({'nomineeName': director_name, 'nomineeLink': director_url})

        is_winner = bool(director_cell.find('b')) or bool(film_cell.find('b'))
        winner_status = "yes" if is_winner else "no"

        entry_data = {
            'movieTitle': movie_title,
            'releaseYear': current_year,
            'categoryName': "Best International Feature Film",
            'iteration': current_iteration,
            'nominees': nominees_info,
            'winner': winner_status
        }

        data.append(entry_data)

with open('best_international_feature.csv', mode='w', encoding='utf-8', newline='') as file1:
    writer1 = csv.writer(file1)
    writer1.writerow(['firstName', 'lastName', 'movieTitle', 'releaseYear',
                      'categoryName', 'iteration', 'winner'])
    for entry in data:
        for nominee in entry['nominees']:
            full_name_parts = nominee['nomineeName'].split(" ", 1)
            first_name = full_name_parts[0]
            last_name = full_name_parts[1] if len(full_name_parts) > 1 else ""

            writer1.writerow([
                first_name,
                last_name,
                entry['movieTitle'],
                entry['releaseYear'],
                entry['categoryName'],
                entry['iteration'],
                entry['winner']
            ])

print(f"Total unique people links collected: {len(PeopleLinks)}")