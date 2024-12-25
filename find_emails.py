import os
import re
import requests
from bs4 import BeautifulSoup
import time
import random
import pandas as pd
from urllib.parse import unquote
import shutil

def fetch_contact_info(name, max_depth=4, retries=6, delay=10):

    def extract_contacts_from_page(url):
        for _ in range(retries):
            try:
                response = requests.get(url, headers=headers, timeout=10, verify=False)
                print(response)
                if response.status_code == 200:
                    page_soup = BeautifulSoup(response.text, 'html.parser')
                    page_text = page_soup.get_text()
                    page_emails = re.findall(email_regex, page_text)
                    page_phones = re.findall(phone_regex, page_text)

                    print(f"Found emails: {page_emails}")
                    print(f"Found phones: {page_phones}")

                    return set(page_emails), set(page_phones)
                elif response.status_code == 429:
                    print(f"Rate limited! Retrying after {delay} seconds...")
                    print(response)

                    time.sleep(delay)
            except requests.exceptions.RequestException as e:
                print(f"Error while requesting {url}: {e}")
                time.sleep(delay)
        print(f"Failed to fetch: {url}")
        return set(), set()

    search_url = f"https://www.google.com/search?q={name} contato"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    email_regex = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    phone_regex = r'\+?55?\s?\(?\d{2}\)?[\s-]?\d{4,5}[\s-]?\d{4}'

    emails = set()
    phones = set()
    visited_links = set()

    for _ in range(retries):
        try:
            response = requests.get(search_url, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                all_links = []
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if 'url?esrc=s&q=&rct=j&sa=U&url=' in href:  # Updated Google redirect link format
                        target_url = href.split('url=')[1].split('&')[0]

                        target_url = unquote(target_url)

                        if not target_url.startswith('http'):
                            target_url = 'https://' + target_url

                        all_links.append(target_url)

                def visit_links(links, depth):
                    if depth == 0:
                        return
                    for link in links:
                        if link not in visited_links:
                            visited_links.add(link)
                            sub_emails, sub_phones = extract_contacts_from_page(link)
                            emails.update(sub_emails)
                            phones.update(sub_phones)

                            time.sleep(random.uniform(1, 3))

                            visit_links([link], depth - 1)

                print(f"Links to follow: {all_links}")
                visit_links(all_links, max_depth)

                print(f"Found emails: {emails}")
                print(f"Found phones: {phones}")
                return {
                    'emails': list(emails),
                    'phones': list(phones)
                }
            elif response.status_code == 429:
                print(f"Rate limited! Retrying after {delay} seconds...")
                time.sleep(delay)
        except requests.exceptions.RequestException as e:
            print(f"Error while requesting Google search URL: {e}")
            time.sleep(delay)

    print(f"Failed to fetch contact info for: {name}")
    return {
        'emails': list(emails),
        'phones': list(phones)
    }

current_folder = os.path.dirname(os.path.abspath(__file__))
csv_files = [f for f in os.listdir(current_folder) if f.endswith('.csv')]

if len(csv_files) != 1:
    print(f"Expected exactly one CSV file in the folder, found {len(csv_files)}.")
    exit(1)

csv_file = csv_files[0]

df = pd.read_csv(os.path.join(current_folder, csv_file))

MAX_DEPTH = 4

for index, row in df.iterrows():
    name = row['nome_entidade_coletivo_cultural']
    email = row['email_publico']
    phone = row['telefone_publico']

    if (not email or email == "Não Informado") and (not phone or phone == "Não Informado"):
        print(f"Fetching contact info for: {name}")

        contact_info = fetch_contact_info(name, MAX_DEPTH)

        if contact_info:
            if contact_info['emails']:
                df.at[index, 'email_publico'] = contact_info['emails'][:4]
            if contact_info['phones']:
                df.at[index, 'telefone_publico'] = contact_info['phones'][:4]
        else:
            print(f"No contact info found for: {name}")

output_folder = os.path.join(current_folder, 'updated_contacts')
os.makedirs(output_folder, exist_ok=True)

output_csv_path = os.path.join(output_folder, 'updated_contacts.csv')
df.to_csv(output_csv_path, index=False)

print(f"Contact information updated and saved to '{output_csv_path}'.")
