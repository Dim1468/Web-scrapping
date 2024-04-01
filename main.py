import json
from unicodedata import normalize
import requests
import bs4
from fake_headers import Headers
import time
from pprint import pprint

keywords = ['Django', 'Flask']

headers_gen = Headers(browser='chrome', os='win')
url = 'https://spb.hh.ru/search/vacancy?ored_clusters=true&hhtmFrom=vacancy_search_list&search_field=name&search_field=company_name&search_field=description&enable_snippets=false&L_save_area=true&area=1&area=2&text=python+flask+django'
response = requests.get(url, headers=headers_gen.generate())
response.raise_for_status()  
main_soup = bs4.BeautifulSoup(response.text, 'lxml')

applications = main_soup.find('main', class_='vacancy-serp-content').find_all('div', class_='serp-item')

parsed_data = []

for application in applications:
    header = application.find('h3').text
    link_tag = application.find('a', class_='serp-item__title')
    link = link_tag['href'] if link_tag else 'Link not found'
    company_name = normalize('NFKD', application.find('a', class_='bloko-link bloko-link_kind-tertiary').text)
    city_name = application.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).text.strip()
    salary_tag = application.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
    salary = normalize('NFKD', salary_tag.text) if salary_tag else 'Не указана'

    parsed_data.append({
        'link': link,
        'header': header,
        'company-name': company_name,
        'city': city_name,
        'salary': salary
    })
    time.sleep(0.1)

if __name__ == '__main__':
    with open('parsed-data.json', 'w', encoding='utf-8') as file:
        json.dump(parsed_data, file, ensure_ascii=False, indent=4)
pprint(parsed_data)


