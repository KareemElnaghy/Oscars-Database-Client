from bs4 import BeautifulSoup
import requests
import csv
import re
from urllib.parse import urlparse
import calendar

def extract_career_years(years_text):
    years_text = re.sub(r"\s*–\s*", "–", years_text)
    years_text = re.sub(r"\s*-\s*", "–", years_text)
    years_text = re.sub(r"\(.*?\)", "", years_text)
    year_ranges = re.split(r";|and", years_text)
    all_years = []
    for year_range in year_ranges:
        years = re.findall(r"\b(\d{4}|present)\b", year_range)
        all_years.extend(years)
    all_years = [int(year) if year != "present" else None for year in all_years]
    numeric_years = [year for year in all_years if year is not None]
    if numeric_years:
        earliest_year = min(numeric_years)
        latest_year = max(numeric_years) if None not in all_years else None
        return earliest_year, latest_year
    return None, None

def extract_date(date_text):
    date_text = re.sub(r"\(.*?\)", "", date_text).strip()
    match = re.search(r"(\w+)?\s*(\d{1,2})?,?\s*(\d{4})", date_text)
    if match:
        year = match.group(3)
        month = match.group(1) if match.group(1) else "01"
        day = match.group(2) if match.group(2) else "01"
        try:
            month = str(list(calendar.month_name).index(month)) if month.isalpha() else month
        except ValueError:
            month = "01"
        return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
    return None

person_data_basic = []
person_data_roles = []
Roles = set()
MalformedLinks = []
missingData = []

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

for url in PeopleLinks: # PeopleLinks is a set of URLs/ this script ran on Jupyter Notebook
    if not is_valid_url(url):
        MalformedLinks.append(url)
        print(f"Malformed URL: {url}")
        continue

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        first_name, last_name, dob, birth_country, death_date = "", "", "", "", ""
        born_row = soup.find('th', string=re.compile(r'(?i)\bBorn\b[:]?'))

        if born_row:
            born_data = born_row.find_next_sibling('td')
            if born_data:
                dob_span = born_data.find('span', class_='bday')
                raw_dob_text = dob_span.get_text(strip=True) if dob_span else born_data.get_text(strip=True)
                dob = extract_date(raw_dob_text)
                birthplace_div = born_data.find('div', class_='birthplace')
                if birthplace_div:
                    raw_birth_country = birthplace_div.get_text(strip=True)
                else:
                    raw_birth_country = born_data.get_text(separator=" ", strip=True)
                cleaned_location = re.sub(r"\(.*?\)", "", raw_birth_country).strip()
                birth_country = cleaned_location.split(",")[-1].strip()

        nameDiv = soup.find('div', class_='fn')
        if not nameDiv:
            name_th = soup.find('th', class_='infobox-above')
            if name_th:
                nameDiv = name_th.find('div')
        if not nameDiv:
            name_caption = soup.find('caption', class_='infobox-title fn')
            if name_caption:
                nameDiv = name_caption

        if nameDiv:
            full_name = nameDiv.get_text(strip=True)
            name_parts = full_name.split(" ")
            first_name = name_parts[0]
            last_name = name_parts[-1] if len(name_parts) > 1 else ""

        death_row = soup.find('th', string='Died')
        if death_row:
            death_data = death_row.find_next_sibling('td')
            death_date_text = death_data.get_text(strip=True) if death_data else ""
            death_date = extract_date(death_date_text)

        occupations_row = soup.find('th', string=re.compile(r'Occupation(s)?'))
        roles = []
        if occupations_row:
            occupations_data = occupations_row.find_next_sibling('td') or soup.find('td', class_='infobox-data role')
            if occupations_data:
                roles_list = occupations_data.find_all('li')
                if roles_list:
                    roles = [role.get_text(strip=True).title() for role in roles_list]
                else:
                    roles_text = occupations_data.get_text(strip=True)
                    roles = [role.strip().title() for role in roles_text.split(",")]

        Roles.update(roles)

        years_active_row = soup.find('th', string=re.compile(r'Years\s*active'))
        career_start_year, career_end_year = "", ""
        if years_active_row:
            years_active_data = years_active_row.find_next_sibling('td')
            if years_active_data:
                years_text = years_active_data.get_text(strip=True)
                career_start_year, career_end_year = extract_career_years(years_text)

        if first_name is None:
            missingData.append(url)
        person_entry_basic = {
            'firstName': first_name,
            'lastName': last_name,
            'DOB': dob,
            'birthCountry': birth_country,
            'deathDate': death_date,
            'careerStartYYYY': career_start_year,
            'careerEndYYYY': career_end_year,
        }
        person_data_basic.append(person_entry_basic)

        for role in roles:
            person_entry_roles = {
                'firstName': first_name,
                'lastName': last_name,
                'roleType': role,
                'careerStartYYYY': career_start_year,
                'careerEndYYYY': career_end_year,
            }
            person_data_roles.append(person_entry_roles)

    except Exception as e:
        print(f"Error: url {url}: {e}")

with open('person.csv', mode='w', encoding='utf-8', newline='') as file1:
    writer1 = csv.writer(file1)
    writer1.writerow(['firstName', 'lastName', 'DOB', 'birthCountry', 'deathDate',
                      'careerStartYYYY', 'careerEndYYYY'])
    for entry in person_data_basic:
        writer1.writerow([
            entry['firstName'],
            entry['lastName'],
            entry['DOB'],
            entry['birthCountry'],
            entry['deathDate'],
            entry['careerStartYYYY'],
            entry['careerEndYYYY']
        ])

with open('person_role.csv', mode='w', encoding='utf-8', newline='') as file2:
    writer2 = csv.writer(file2)
    writer2.writerow(['firstName', 'lastName', 'roleType', 'careerStartYYYY', 'careerEndYYYY'])
    for entry in person_data_roles:
        writer2.writerow([
            entry['firstName'],
            entry['lastName'],
            entry['roleType'],
            entry['careerStartYYYY'],
            entry['careerEndYYYY']
        ])

print("Unique Roles Collected:")
for role in Roles:
    print(role)
