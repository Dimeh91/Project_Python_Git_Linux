#!/bin/bash
# Exemple de script de scraping pour récupérer le prix du Bitcoin

URL="https://www.coingecko.com/en/coins/bitcoin"
html=$(curl -s "$URL")
price=$(echo "$html" | grep -oE '\$[0-9,]+\.[0-9]+' | head -n 1)

if [ -z "$price" ]; then
    echo "[$(date +"%Y-%m-%d %H:%M:%S")] Erreur : prix non trouvé" >> scraper_error.log
    exit 1
fi

timestamp=$(date +"%Y-%m-%d %H:%M:%S")
mkdir -p data
echo "$timestamp, $price" >> data/bitcoin_prices.csv
