import requests
from bs4 import BeautifulSoup
import csv
import re

url = "https://en.wikipedia.org/wiki/Academy_Award_for_Best_Supporting_Actress"
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

        if len(cols) < 3:
            continue

        actor_cell = cols[0]
        actor_link_tag = actor_cell.find('a')

        if not actor_link_tag:
            continue

        actor_name = actor_link_tag.get_text(strip=True)
        actor_link = f"https://en.wikipedia.org{actor_link_tag['href']}"
        PeopleLinks.add(actor_link)

        film_cell = cols[2] if len(cols) > 2 else None
        film_title_tag = film_cell.find('i') if film_cell else None
        film_title_link_tag = film_title_tag.find('a') if film_title_tag else None

        film_title = (
            film_title_link_tag.get_text(strip=True)
            if film_title_link_tag
            else (film_title_tag.get_text(strip=True) if film_title_tag else None)
        )

        if not film_title:
            continue

        is_winner = bool(actor_cell.find('b')) or bool(film_cell.find('b'))
        winner_status = "yes" if is_winner else "no"

        entry_data = {
            'movieTitle': film_title,
            'releaseYear': current_year,
            'categoryName': "Best Actress in a Supporting Role",
            'iteration': current_iteration,
            'isWinner': winner_status,
            'actor': {
                'firstName': actor_name.split(" ", 1)[0],
                'lastName': actor_name.split(" ", 1)[1] if " " in actor_name else "",
                'link': actor_link
            }
        }

        data.append(entry_data)

with open('best_supporting_actress.csv', mode='w', encoding='utf-8', newline='') as file1:
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

print(f"Total unique people links collected: {len(PeopleLinks)}")