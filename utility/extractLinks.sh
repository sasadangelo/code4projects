#!/bin/bash

# Verifichiamo che sia stato passato esattamente un argomento
if [ "$#" -ne 1 ]; then
  # Stampiamo un messaggio di errore e lo usage corretto
  echo "Errore: è richiesto un URL"
  echo "Usage: $0 URL"
  exit 1
fi

# Prendiamo l'URL del sito web come argomento dello script
url=$1

# Inizializziamo la variabile che conterrà la lista degli URL già analizzati
processed_urls=()

# Funzione ricorsiva per estrarre i link da tutte le pagine del sito web
function extract_links {
  # Prendiamo l'URL della pagina web come argomento della funzione
  url=$1

  # Verifichiamo se l'URL è già stato analizzato
  if [[ " ${processed_urls[@]} " =~ " ${url} " ]]; then
    # Se l'URL è già stato analizzato, non facciamo nulla
    return
  fi

  # Aggiungiamo l'URL alla lista degli URL già analizzati
  processed_urls+=("$url")

  # Estraiamo tutti i link dalla pagina web specificata dall'URL
  all_links=$(fetchURL.sh -a "$url")

  # Iteriamo sulla lista dei link
  for link in $links; do
    # Richiamiamo la funzione per estrarre i link dalla nuova pagina web
    extract_links "$link"
  done
}

# Richiamiamo la funzione per iniziare l'estrazione dei link dal sito web specificato dall'URL
extract_links "$url"

