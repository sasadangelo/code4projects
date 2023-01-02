import requests
from bs4 import BeautifulSoup

# Funzione per verificare che il titolo abbia meno di 53 caratteri
def check_title_length(soup):
    # Cerchiamo il tag title nella pagina HTML
    title = soup.find("title")
    # Se il tag title esiste e ha meno di 53 caratteri, ritorniamo True
    if title and len(title.text) < 53:
        return True
    # Altrimenti, ritorniamo False
    return False

# Funzione per verificare che ci sia un solo tag h1
def check_single_h1(soup):
    # Cerchiamo tutti i tag h1 nella pagina HTML
    h1_tags = soup.find_all("h1")
    # Se c'è un solo tag h1, ritorniamo True
    if len(h1_tags) == 1:
        return True
    # Altrimenti, ritorniamo False
    return False

# Funzione per verificare che se c'è un tag h2 allora ci deve essere per forza un tag h1
def check_h2_requires_h1(soup):
    # Cerchiamo tutti i tag h1 e h2 nella pagina HTML
    h1_tags = soup.find_all("h1")
    h2_tags = soup.find_all("h2")
    # Se c'è almeno un tag h2 e almeno un tag h1, ritorniamo True
    if len(h2_tags) == 0:
        return True
    if len(h2_tags) >= 1 and len(h1_tags) >= 1:
        return True
    # Altrimenti, ritorniamo False
    return False

# Funzione per verificare che la meta description abbia una lunghezza compresa tra 106 e 142 caratteri
def check_meta_description_length(soup):
    # Cerchiamo il tag meta con attributo name "description" nella pagina HTML
    meta_description = soup.find("meta", attrs={"name": "description"})
    # Se il tag meta esiste e ha una lunghezza compresa tra 106 e 142 caratteri, ritorniamo True
    if meta_description and 106 <= len(meta_description["content"]) <= 142:
        return True
    # Altrimenti, ritorniamo False
    return False

# Prendiamo l'URL del sito web come input dello script
url = input("Inserisci l'URL del sito web: ")

# Scarichiamo il contenuto della pagina web specificata dall'URL
page = requests.get(url)

# Verifichiamo che la richiesta sia stata eseguita con successo
if page.status_code == 200:
    # Inizializziamo BeautifulSoup con il contenuto della pagina HTML
    soup = BeautifulSoup(page.content, "html.parser")

    # Verifichiamo che il titolo abbia meno di 53 caratteri
    if check_title_length(soup):
        print("Title: OK!")
    else:
        print("Title: KO!")

    # Verifichiamo che ci sia un solo tag H1
    if check_single_h1(soup):
        print("H1: OK!")
    else:
        print("H1: KO!")

    # Verifichiamo che se c'è almeno un tag H2 allora ci deve essere un tag H1
    if check_h2_requires_h1(soup):
        print("H2: OK!")
    else:
        print("H2: KO!")

    # Verifichiamo che la meta description esista e abbia una lunghezza compresa tra 106 e 142 caratteri.
    if check_meta_description_length(soup):
        print("Meta description: OK!")
    else:
        print("Meta description: KO!")

else:
    print("Errore nello scaricamento della pagina web.")
