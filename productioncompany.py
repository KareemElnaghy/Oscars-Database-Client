import requests
from bs4 import BeautifulSoup
import csv
import re
import time
import random

def extract_company(infobox):
    if not infobox:
        return None

    rows = infobox.find_all('tr')  # Find all rows in the infobox

    for row in rows:
        header = row.find('th', class_='infobox-label')  # Target headers with class 'infobox-label'

        if header:
            div = header.find('div')

            # Normalize text by removing newlines and spaces, and check for "Production company"
            normalized_text = div.text.replace('\n', '').replace(' ', '').lower() if div else ''
            if 'productioncompany' in normalized_text:  # Check for "Production company"
                company_cell = row.find('td')  # Find the corresponding <td> cell
                if company_cell:
                    # Extract all company names from lists or directly from text
                    companies = []
                    for ul in company_cell.find_all('ul'):  # Check for <ul> lists
                        for li in ul.find_all('li'):  # Extract each <li> item
                            company_name = li.get_text(strip=True)
                            companies.append(company_name)
                    if not companies:  # If no <ul>, check for direct links or text
                        for a in company_cell.find_all('a'):
                            company_name = a.get_text(strip=True)
                            companies.append(company_name)
                        if not companies:  # If no links, extract plain text
                            companies.append(company_cell.get_text(strip=True))
                    return ', '.join(companies)  # Return all companies as a comma-separated string

            elif 'productioncompanies' in normalized_text:  # Check for "Production Companies"
                company_cell = row.find('td')  # Find the corresponding <td> cell
                if company_cell:
                    companies = []
                    for ul in company_cell.find_all('ul'):  # Check for <ul> lists
                        for li in ul.find_all('li'):  # Extract each <li> item
                            company_name = li.get_text(strip=True)
                            companies.append(company_name)
                    if not companies:  # If no <ul>, check for direct links or text
                        for a in company_cell.find_all('a'):
                            company_name = a.get_text(strip=True)
                            companies.append(company_name)
                        if not companies:  # If no links, extract plain text
                            companies.append(company_cell.get_text(strip=True))
                    return ', '.join(companies)  # Return all companies as a comma-separated string

    return None





# Fetch the main Wikipedia page listing nominated films
url = "https://en.wikipedia.org/wiki/List_of_Academy_Award%E2%80%93nominated_films"
headers = {'User-Agent': 'Mozilla/5.0 (compatible; AcademyAwardScraper/1.0)'}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# Prepare data storage
movie_data = []

# Find all wikitable tables on the page
tables = soup.find_all('table', class_=lambda x: x and 'wikitable' in x)

for table in tables:
    rows = table.find_all('tr')[1:]  # Skip header row

    for row in rows:
        cols = row.find_all(['td', 'th'])

        # Skip invalid rows
        if len(cols) < 3:
            continue

        # Extract movie title and release year from the main table
        movie_title_link = cols[0].find('a')
        if movie_title_link:
            movie_title = movie_title_link.text.strip()
            movie_url = "https://en.wikipedia.org" + movie_title_link['href']
        else:
            continue  # Skip if no link

        release_year = cols[1].text.strip()

        # Fetch individual movie's Wikipedia page to get production company
        try:
            movie_response = requests.get(movie_url, headers=headers)
            movie_soup = BeautifulSoup(movie_response.content, 'html.parser')

            infobox = movie_soup.find('table', class_=lambda x: x and 'infobox' in x)
            
            company_name = extract_company(infobox)

            if company_name is None:
                cleaned_company_names = ['']
            else:  
                cleaned_company_names = [re.sub(r'\[\d+\]', '', name).strip() for name in company_name.split(', ')]
            

            print(f"Movie: {movie_title}")
            print(f"Release Year: {release_year}")
            print(f"Production Company: {cleaned_company_names}\n")

            movie_data.append({
                'movieTitle': movie_title,
                'releaseYear': release_year,
                'companyName': cleaned_company_names
            })
            

            # Randomized delay between requests (1 to 3 seconds)
            time.sleep(random.uniform(1, 3))

        except Exception as e:
            print(f"Failed to fetch {movie_title}: {e}")
            continue

        with open('test.csv', mode='w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Movie Title', 'Release Year', 'Production Company'])

with open('oscar_nominated_movies_companies.csv', mode='w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Movie Title', 'Release Year', 'Production Company'])

    for entry in movie_data:
        for comp in entry['companyName']:
            writer.writerow([
                entry['movieTitle'],
                entry['releaseYear'],
                comp
            ])

print("Movie production companies saved to 'oscar_nominated_movies_companies.csv'")