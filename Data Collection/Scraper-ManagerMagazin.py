from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import re

def scrape_links(links, output_filename):
    # Setze die Optionen für den Chrome WebDriver
    chrome_options = ChromeOptions()

    # Deaktiviere das Cookie-Plugin
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-plugins')

    # Webdriver initialisieren
    driver = webdriver.Chrome(options=chrome_options)

    scraped_data = []

    for link in links:
        # Öffne die Seite
        driver.get(link)

        # Warte, bis die Seite geladen ist
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'suchergebnisse')))

        # Hole den HTML-Inhalt nach dem Warten auf die dynamische Aktualisierung der Seite
        html_content = driver.page_source

        # BeautifulSoup initialisieren
        soup = BeautifulSoup(html_content, 'html.parser')

        # Ziel-HTML-Element finden
        target_section = soup.find('section', {'aria-label': 'Suchergebnisse', 'id': 'suchergebnisse'})

        # Extrahiere die gewünschten Daten
        if target_section:
            # Hier sucht der Code nach allen <article> innerhalb der gefundenen <section>
            articles = target_section.find_all('article', {'aria-label': True})

            for article in articles:
                # Überprüfe, ob das Element vorhanden ist, bevor auf .text zugegriffen wird
                h2_element = article.find('h2', {'class': 'w-full'})
                if h2_element:
                    title_span = h2_element.find('span', {'class': 'align-middle'})
                    title = title_span.text.strip() if title_span else ''
                else:
                    title = ''

                link_element = article.find('a')
                link = link_element['href'].strip() if link_element else ''

                date_element = article.find('footer').find('span', {'data-auxiliary': ''})
                date = date_element.text.strip() if date_element else ''

                # Extrahiere die Lesezeit
                reading_time_element = article.find('span', {'data-icon-auxiliary': 'Text', 'class': 'flex items-center'})
                reading_time_text = reading_time_element.find('span').text.strip() if reading_time_element else ''
                # Extrahiere die Zahl aus dem Lesezeit-Text mit einem regulären Ausdruck
                reading_time_match = re.search(r'\b(\d+)\s*Min\b', reading_time_text)
                reading_time = reading_time_match.group(1) if reading_time_match else ''

                # Extrahiere den Kurztext
                short_text_element = article.find('span', {'class': 'font-serifUI font-normal text-base leading-loose mr-6', 'data-target-teaser-el': 'text'})
                short_text = short_text_element.text.strip() if short_text_element else ''

                result = {
                    'title': title,
                    'link': link,
                    'date': date,
                    'reading_time': reading_time,
                    'short_text': short_text
                }

                scraped_data.append(result)

    # Schließe den WebDriver
    driver.quit()

    # JSON-Datei schreiben
    with open(output_filename, 'w', encoding='utf-8') as json_file:
        json.dump(scraped_data, json_file, ensure_ascii=False, indent=2)

    print(f"Scraping abgeschlossen. Daten wurden in '{output_filename}' gespeichert.")

# Verwende die zuvor gespeicherten Links aus mm_links.json
manager_magazin_links = json.load(open('mm_links.json'))

# Scrape die Daten und speichere sie in einer JSON-Datei
scrape_links(manager_magazin_links, 'mm_search_results.json')
