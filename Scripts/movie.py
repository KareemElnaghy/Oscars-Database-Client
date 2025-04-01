import requests
from bs4 import BeautifulSoup
import csv
import re
import time

def clean_runtime(runtime_str):
    # Remove any non-digit characters except for spaces, commas, hyphens, and question marks
    cleaned_str = re.sub(r'[^\d\s,\-\?]', '', runtime_str)
    cleaned_str = cleaned_str.replace('?', '')
    runtimes = re.split(r'[,\s]+', cleaned_str)
    first_runtime = runtimes[0]

    # handle runtime ranges like 130-154
    if '-' in first_runtime:
        first_runtime = first_runtime.split('-')[0]

    # handle format like "8:11"
    if ':' in first_runtime:
        parts = first_runtime.split(':')
        minutes = int(parts[0]) + int(parts[1]) / 60
        return round(minutes * 60)

    # convert to minutes if it's in hours and minutes format
    if 'h' in first_runtime:
        match = re.search(r'(\d+)h\s*(\d+)m', first_runtime)
        if match:
            hours = int(match.group(1))
            minutes = int(match.group(2))
            return hours * 60 + minutes
        else:
            match = re.search(r'(\d+)h', first_runtime)
            if match:
                hours = int(match.group(1))
                return hours * 60
    elif 'm' in first_runtime:
        return int(re.sub(r'[^\d]', '', first_runtime))
    else:
        return int(first_runtime)

def convert_to_number(value_str):
    cleaned_str = re.sub(r'[\$,]', '', value_str)

    match = re.search(r'(\d+(?:\.\d+)?)\s*(million|billion)?', cleaned_str, re.IGNORECASE)

    if match:
        value = float(match.group(1))
        unit = match.group(2)

        if unit == 'million':
            return value * 1e6
        elif unit == 'billion':
            return value * 1e9
        else:
            return value
    else:
        return None

def clean_language(language_str):
    cleaned_str = re.sub(r'[^\w\s]', '', language_str)
    words = cleaned_str.split()

    if words:
        return words[0]
    else:
        return 'Unknown'

url = "https://en.wikipedia.org/wiki/List_of_Academy_Award%E2%80%93nominated_films"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

movie_data = []
sound_films_started = False

# Find all wikitable tables on the page
tables = soup.find_all('table', class_=lambda x: x and 'wikitable' in x)

for table in tables:
    rows = table.find_all('tr')[1:]  # Skip header row

    for row in rows:
        cols = row.find_all(['td', 'th'])

        if len(cols) < 3:
            continue

        movie_title_link = cols[0].find('a')
        if movie_title_link:
            movie_title = movie_title_link.text.strip()
            movie_url = "https://en.wikipedia.org" + movie_title_link['href']
        else:
            movie_title = cols[0].text.strip()
            continue

        release_year = cols[1].text.strip()

        if movie_title == "White Shadows in the South Seas":
            sound_films_started = True

        movie_response = requests.get(movie_url)
        movie_soup = BeautifulSoup(movie_response.content, 'html.parser')

        details = {
            'movieTitle': movie_title,
            'releaseYear': release_year,
            'language': None,
            'runtime': None,
            'budget': None,
            'boxOffice': None
        }

        info_box = movie_soup.find('table', class_=lambda x: x and 'infobox' in x)
        if info_box:
            rows = info_box.find_all('tr')
            for row in rows:
                cols = row.find_all(['th', 'td'])
                if len(cols) > 1:
                    if cols[0].text.strip() == 'Language':
                        if sound_films_started:
                            details['language'] = clean_language(cols[1].text.strip())
                        else:
                            details['language'] = 'Silent'
                    elif cols[0].text.strip() == 'Running time':
                        details['runtime'] = clean_runtime(cols[1].text.strip())
                    elif cols[0].text.strip() == 'Budget':
                        details['budget'] = convert_to_number(cols[1].text.strip())
                    elif cols[0].text.strip() == 'Box office':
                        details['boxOffice'] = convert_to_number(cols[1].text.strip())

        movie_data.append(details)


with open('oscar_nominated_movies.csv', mode='w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Movie Title', 'Release Year', 'Language', 'Runtime', 'Budget', 'Box Office'])

    for entry in movie_data:
        writer.writerow([
            entry['movieTitle'],
            entry['releaseYear'],
            entry['language'],
            entry['runtime'],
            entry['budget'],
            entry['boxOffice']
        ])

print("Movie data saved to 'oscar_nominated_movies.csv'")
