import requests
from bs4 import BeautifulSoup
import csv
import re

def extract_company(infobox):
    if not infobox:
        return None

    rows = infobox.find_all('tr')

    for row in rows:
        header = row.find('th', class_='infobox-label')

        if header:
            div = header.find('div')
            normalized_text = div.text.replace('\n', '').replace(' ', '').lower() if div else ''
            if 'productioncompany' in normalized_text:
                company_cell = row.find('td')
                if company_cell:
                    companies = []
                    for ul in company_cell.find_all('ul'):
                        for li in ul.find_all('li'):
                            company_name = li.get_text(strip=True)
                            companies.append(company_name)
                    if not companies:
                        for a in company_cell.find_all('a'):
                            company_name = a.get_text(strip=True)
                            companies.append(company_name)
                        if not companies:
                            companies.append(company_cell.get_text(strip=True))
                    return ', '.join(companies)

            elif 'productioncompanies' in normalized_text:
                company_cell = row.find('td')
                if company_cell:
                    companies = []
                    for ul in company_cell.find_all('ul'):
                        for li in ul.find_all('li'):
                            company_name = li.get_text(strip=True)
                            companies.append(company_name)
                    if not companies:
                        for a in company_cell.find_all('a'):
                            company_name = a.get_text(strip=True)
                            companies.append(company_name)
                        if not companies:
                            companies.append(company_cell.get_text(strip=True))
                    return ', '.join(companies)

    return None


url = "https://en.wikipedia.org/wiki/List_of_Academy_Award%E2%80%93nominated_films"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

movie_data = []

tables = soup.find_all('table', class_=lambda x: x and 'wikitable' in x)

for table in tables:
    rows = table.find_all('tr')[1:]

    for row in rows:
        cols = row.find_all(['td', 'th'])

        if len(cols) < 3:
            continue

        movie_title_link = cols[0].find('a')
        if movie_title_link:
            movie_title = movie_title_link.text.strip()
            movie_url = "https://en.wikipedia.org" + movie_title_link['href']
        else:
            continue

        release_year = cols[1].text.strip()


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


with open('production_company.csv', mode='w', encoding='utf-8', newline='') as file:
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