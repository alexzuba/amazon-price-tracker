import requests
from bs4 import BeautifulSoup
import re


#Devo mettere un for iniziale che cicla per ogni riga di un txt, che sarà il txt in cui metto i link che voglio tracciare. Prima devo riuscire ad accedere al nome dell'oggetto + il prezzo, e poi man mano li appendo in un file di testo
PRINT_DEBUG = True

custom_headers = { #Header per evitare captcha
    "Accept-language": "en-GB,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
}

#Devo aggiungere un check per controllare che la lettura dell'URL sia andata a buon fine, altrimenti riprovare

#Parte iniziale dove scrivo gli oggetti/prezzi nuovi
new_prices = open('new_prices.txt', 'w', encoding='utf-8', newline='') #Apro e chiudo il file con 'w' per cancellarlo
new_prices.close()
new_prices = open('new_prices.txt', 'a', encoding='utf-8', newline='') #Apro il file con 'a' per fare append
product_list = open('product_list.txt', 'r')
lines = product_list.readlines()
i = 0
for line in lines:
    URL = line
    print(i)
    i = i + 1
    print(URL)
    #page = requests.get(URL)
    page = requests.get(URL, headers=custom_headers)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="content") #Funziona, ottengo la parte delle pizze
    #f = open("tmp.txt", 'w', encoding='utf-8')

    #Parte per scrivere HTML in file, funzionante:
    #f = open("tmp.html", 'w', encoding='utf-8')
    #x = soup.prettify()
    #f.write(x)
    #f.close()

    #Printo il titolo
    new_prices.write("OGGETTO: ")
    title = soup.select('meta[name="title"]')
    if PRINT_DEBUG == True:
        print(title[0].attrs["content"]) #FUNZIONA, RIESCO A PRINTARE IL TITOLO 
    new_prices.write(title[0].attrs["content"])
    new_prices.write("\nPrezzo: ")
    prezzo_dec = soup.find("span", class_="a-price-whole") #Trova i decimali
    prezzo_fraz = soup.find("span", class_="a-price-fraction")
    print(prezzo_dec.text)
    print(prezzo_fraz.text)
    new_prices.write(prezzo_dec.text)
    new_prices.write(prezzo_fraz.text)
    new_prices.write('\n')
    #Fino a qua funziona, scrive l'oggetto ed il prezzo, ora devo fare in modo che peschi il link da un txt e basta mettere un for, per poi fare un confronto

#Finito di scrivere new_prices.txt, ora va fatto confronto con old_prices per controllare se i vecchi prezzi sono cambiati, e nel caso mandare mail


