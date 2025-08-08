import requests
from bs4 import BeautifulSoup
import re


#Devo mettere un for iniziale che cicla per ogni riga di un txt, che sarà il txt in cui metto i link che voglio tracciare. Prima devo riuscire ad accedere al nome dell'oggetto + il prezzo, e poi man mano li appendo in un file di testo
PRINT_DEBUG = False

#Parte iniziale dove scrivo gli oggetti/prezzi nuovi
new_prices = open('new_prices.txt', 'w', encoding='utf-8', newline='')


URL = "https://www.amazon.it/PROIRON-Giubbotto-regolabile-riflettente-allenamento/dp/B09QXGQNFC/ref=sr_1_2_sspa?__mk_it_IT=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=1TQAX9YAKVNMI&dib=eyJ2IjoiMSJ9.rdynVfwpfPyhcWfQVn9j2Z9eJcoQ4wmK7S4hMSYUu9BsRSuhM_zc8D2M-6hGBXtDUJ-MRVH-KiKrSDxGU-mYQYdc3LrSPkcjteEMRvGr6LMmuo9BQbvFug9n4as80cDwaWvrnqWmn_vVYHlYA_cPbI5KeaLtfkC269rBEq9VY9loz1EAwcE6fK2v71mp1AXUuKOKe73C4PQ4XHwyG1WK4jZFJc51AEGIu_QACRojgu79mjRQg7Ftp67L_1vc7vtiKrXtiQm8FNDNuNIm7ROBlvKeVV7hc0JzEaBwsdPqJCo.GKjzqdThssrrq1LxO_2lk5c24Vk4kMXcA89CqP03S5g&dib_tag=se&keywords=ceste%2Bpesi&qid=1754512565&sprefix=vest%2Bpesi%2Caps%2C159&sr=8-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1"
page = requests.get(URL)

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
#Fino a qua funziona, scrive l'oggetto ed il prezzo, ora devo fare in modo che peschi il link da un txt e basta mettere un for, per poi fare un confronto


