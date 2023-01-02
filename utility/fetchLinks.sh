#!/bin/bash

# Verifichiamo che siano stati passati esattamente due argomenti
if [ "$#" -ne 2 ]; then
  # Stampiamo un messaggio di errore e lo usage corretto
  echo "Errore: è richiesto un URL e un'opzione"
  echo "Usage: $0 URL opzione"
  exit 1
fi

# Prendiamo l'URL del sito web come primo argomento dello script
# e il secondo argomento come opzione per filtrare gli URL
url=$2
option=$1

# Scarichiamo il contenuto della pagina web usando wget
wget -qO- $url > page.html

# Estraiamo i link dal contenuto della pagina
links=$(grep -o '<a .*href=.*>' page.html | sed -e 's/<a /\n<a /g' | sed -e 's/<a .*href=['"'"'"]//' -e 's/["'"'"'].*$//' -e '/^$/ d')

# Aggiungiamo l'URL in input all'inizio degli URL relativi
processed_links=$(echo "$links" | sed "s|^/|$url/|")

# Rimuoviamo i duplicati dalla lista dei link e i link locali
unique_links=$(echo "$processed_links" | grep -v "#" | sort -u)

# Inizializziamo la variabile che conterrà gli URL modificati
#modified_urls=""

for link in $unique_links
do
  echo "$link"
done


# Iteriamo sugli argomenti passati allo script
#for url in "$unique_links"; do
  # Verifichiamo se l'URL inizia con http:// o https://
#  if [[ $url =~ ^https?:// ]]; then
    # Estraiamo il dominio dall'URL
#    domain=$(echo "$url" | awk -F[/:] '{print $4}')
    # Verifichiamo se il dominio inizia con "www."
#    if [[ $domain =~ ^www. ]]; then
      # Se il dominio inizia con "www.", aggiungiamo l'URL invariato alla variabile
#      modified_urls="$modified_urls$url"$'\n'
#    else
      # Se il dominio non inizia con "www.", aggiungiamo "www." all'URL e aggiungiamo il nuovo URL alla variabile
#      new_url="${url/\/$domain/\/www.$domain}"
#      modified_urls="$modified_urls$new_url"$'\n'
#    fi
#  else
    # Se l'URL non inizia con http:// o https://, stampiamo un messaggio di errore
#    echo "Errore: URL $url non valido"
#  fi
#done


# Filtriamo gli URL in base all'opzione specificata
#case $option in
#  -i|--internal)
    # Stampiamo solo gli URL interni al sito web in input
#    echo "$unique_links" | grep "^$url"
#    ;;
#  -e|--external)
    # Stampiamo solo gli URL esterni al sito web in input
#    echo "$unique_links" | grep -v "^$url"
#    ;;
#  -a|--all)
    # Stampiamo tutti gli URL, sia interni che esterni
#    echo "$unique_links"
#    ;;
#  *)
    # Stampiamo un messaggio di errore e lo usage corretto
    # se l'opzione non è riconosciuta
#    echo "Errore: opzione non riconosciuta"
#    echo "Usage: $0 URL"
#esac

# Rimuoviamo il file temporaneo con il contenuto della pagina
rm page.html
