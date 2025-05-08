import requests
from bs4 import BeautifulSoup
import csv
import re

url = "https://en.wikipedia.org/wiki/Academy_Award_for_Best_Animated_Feature"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

data = []
PeopleLinks = set()

tables = soup.find_all('table', class_='wikitable')

current_year = None
current_iteration = None

for table in tables:
    rows = table.find_all('tr')[1:]

    for row in enumerate(rows):
        cols = row.find_all(['td', 'th'])

        if cols and cols[0].name == 'th':
            year_text = cols[0].get_text(strip=True)
            match_year = re.search(r'(\d{4})', year_text)
            match_iteration = re.search(r'\((\d+(?:st|nd|rd|th))\)', year_text)

            if match_year:
                current_year = int(match_year.group(1))
            if match_iteration:
                current_iteration = match_iteration.group(1)

            if len(cols) > 2:
                film_cell = cols[1]
                nominee_cell = cols[2]
            else:
                continue
        else:
            if len(cols) < 2:
                continue

            film_cell = cols[0]
            nominee_cell = cols[1]

        film_title_tag = film_cell.find('i')
        if not film_title_tag:
            continue

        film_title_link_tag = film_title_tag.find('a')
        movie_title = (
            film_title_link_tag.get_text(strip=True)
            if film_title_link_tag
            else film_title_tag.get_text(strip=True)
        )

        is_winner = bool(film_cell.find('b')) or "background:#FAEB86" in str(row) or "‡" in film_cell.get_text()
        winner_status = "yes" if is_winner else "no"

        nominees_info = []
        nominee_links = nominee_cell.find_all('a')

        for link in nominee_links:
            nominee_name = link.get_text(strip=True)
            nominee_url = f"https://en.wikipedia.org{link['href']}"
            nominees_info.append({
                'nomineeName': nominee_name,
                'nomineeLink': nominee_url
            })
            PeopleLinks.add(nominee_url)

        entry_data = {
            'movieTitle': movie_title,
            'releaseYear': current_year,
            'categoryName': "Best Animated Feature Film",
            'iteration': current_iteration,
            'isWinner': winner_status,
            'nominees': nominees_info
        }

        data.append(entry_data)

with open('best_animated_feature.csv', mode='w', encoding='utf-8', newline='') as file1:
    writer1 = csv.writer(file1)
    writer1.writerow(['firstName', 'lastName', 'movieTitle', 'releaseYear',
                      'categoryName', 'iteration', 'isWinner'])
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
                entry['isWinner']
            ])

print(f"Total unique people links collected: {len(PeopleLinks)}")