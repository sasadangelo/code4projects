from urllib.parse import urlparse
import argparse
import requests
from bs4 import BeautifulSoup

def get_domain(url):
  # Esegue il parsing dell'URL
  parsed_url = urlparse(url)

  # Restituisce il dominio dell'URL
  return parsed_url.netloc

# Funzione per unire l'URL in input con un link che inizia con /
def add_url_to_link(url, link):
    # Se il link inizia con /, aggiungiamo l'URL in input all'inizio del link
    if link.startswith("/"):
        return url + link
    # Altrimenti, ritorniamo il link senza modifiche
    return link

def print_page_links(url, visited_urls):
    print("Processing URL: " + url)
    # Scarichiamo il contenuto della pagina web specificata dall'URL
    page = requests.get(url)
    domain = get_domain(url)

    # Verifichiamo che la richiesta sia stata eseguita con successo
    if page.status_code == 200:
        # Inizializziamo BeautifulSoup con il contenuto della pagina HTML
        soup = BeautifulSoup(page.content, "html.parser")
        # Cerchiamo tutti i tag a nella pagina HTML
        links = soup.find_all("a")

        # Inizializziamo una lista vuota per contenere i links validi e unici
        unique_links = []
        # Per ogni tag a trovato, verifichiamo che non contenga il carattere # e che 
        # non sia già stato aggiunto alla lista dei links validi
        for link in links:
            href = add_url_to_link(url, link["href"])
            if "#" not in href and href not in unique_links:
                # Aggiungiamo il link valido alla lista dei links validi
                unique_links.append(add_url_to_link(url, href))

        unique_links.sort()

        # Stampiamo la lista dei links validi
        for link in unique_links:
            if link not in printed_urls:
                print(link)
                printed_urls.add(link)

        # Visitiamo ora i link non ancora visitati
        for link in unique_links:
            if link not in visited_urls:
                visited_urls.add(link)
                if domain in url:
                    print_page_links(link, printed_urls, visited_urls)
    else:
        print("Errore nello scaricamento della pagina web.")

# Crea un parser per gestire l'opzione -u o --url
parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', required=True, help='URL della pagina web da analizzare')

# Parse degli argomenti da riga di comando
args = parser.parse_args()

# Prendi l'URL della pagina web dall'argomento della riga di comando
url = args.url

# Crea un insieme vuoto per memorizzare gli URL già stampati
visited_urls = set()
visited_urls.add(url)

print_page_links(url, visited_urls)
