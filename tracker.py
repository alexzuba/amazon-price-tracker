#Parsing HTML
import requests
from bs4 import BeautifulSoup
#Sending Email
import smtplib
from email.mime.text import MIMEText
#Using secret variables
import os

#Possibili miglioramenti: usare un json come file di configurazione anziché un txt 

#Devo mettere un for iniziale che cicla per ogni riga di un txt, che sarà il txt in cui metto i link che voglio tracciare. Prima devo riuscire ad accedere al nome dell'oggetto + il prezzo, e poi man mano li appendo in un file di testo
PRINT_DEBUG = False
SEND_EMAIL_DEBUG = True

custom_headers = { #Header per evitare captcha
    "Accept-language": "en-GB,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
}

#Devo aggiungere un check per controllare che la lettura dell'URL sia andata a buon fine, altrimenti riprovare -> Dopo aver messo gli headers non dovrebbe più servire

#Parte iniziale dove scrivo gli oggetti/prezzi nuovi
new_prices = open('new_prices.txt', 'w', encoding='utf-8', newline='') #Apro e chiudo il file con 'w' per cancellarlo
new_prices.close()
new_prices = open('new_prices.txt', 'a', encoding='utf-8', newline='') #Apro il file con 'a' per fare append
product_list = open('product_list.txt', 'r')
lines = product_list.readlines()
i = 0
for line in lines:
    URL = line
    #print(i)
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
    new_prices.write("Oggetto: ")
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
new_prices.close()

#Confronto con i vecchi prezzi
old_prices = open('old_prices.txt', 'r')
new_prices = open('new_prices.txt', 'r')
changed_prices = open('changed_prices.txt', 'w', newline='') #File in cui scrivo i prezzi cambiati, da inviare per mail. Non c'è '\n' alla fine della riga scritta

old_prices_data = old_prices.readlines()
new_prices_data  = new_prices.readlines()
i = 0
update = 0 #Se rimane a 0 non c'è bisogno di sovrascrivere old_prices, altrimenti devo sovrascriverlo con new_prices
#Suppongo che il nome dell'oggetto non cambi, quindi controllo solo le righe dispari
for line1, line2 in zip(old_prices_data, new_prices_data):
    #Se i non dà resto, sto controllando il nome dell'oggeto, li salvo 
    if((i % 2) == 0):
        line1_old = line1
        line2_old = line2
        i += 1
        continue
    else:
        i += 1
        if line1 == line2:
            i = i #Do nothing
        else:
            if PRINT_DEBUG == True:
                print(f"Line {i}:")
                print(f"\tVecchio prezzo: {line1.strip()}")
                print(f"\tNuovo prezzo: {line2.strip()}")
            #Possibile bug: se due oggetti sono diversi (nome) ma hanno lo stesso prezzo, questo non funzionerebbe. Ma non dovrebbe succedere per come si scrive il file product_list.txt
            changed_prices.write("Vecchio oggetto: ")
            changed_prices.write(line1_old)
            changed_prices.write("Vecchio prezzo: ")
            changed_prices.write(line1)
            changed_prices.write("Nuovo oggetto: ")
            changed_prices.write(line2_old)
            changed_prices.write("Nuovo prezzo: ")
            changed_prices.write(line2)
            changed_prices.write('\n') 
            update = 1
old_prices.close()
new_prices.close()
changed_prices.close()

#Sovrascrivo old_prices se new_prices /= old_prices
if update == 1:
    i = 0
    old_prices = open('old_prices.txt', 'w')
    new_prices = open('new_prices.txt', 'r')
    for line in new_prices:
        i += 1
        old_prices.write(line)
old_prices.close()
new_prices.close()

#Mando email
if SEND_EMAIL_DEBUG == True:
    try:
        SECRET_EMAIL_RECEIVER_1 = os.environ["SECRET_EMAIL_RECEIVER_1"]
    except KeyError:
        SECRET_EMAIL_RECEIVER_1 = "Token not available"
        print("Token not available")
    try:
        SECRET_EMAIL_RECEIVER_2 = os.environ["SECRET_EMAIL_RECEIVER_2"]
    except KeyError:
        SECRET_EMAIL_RECEIVER_2 = "Token not available"
        print("Token not available")
    try:
        SECRET_EMAIL_SENDER = os.environ["SECRET_EMAIL_SENDER"]
    except KeyError:
        SECRET_EMAIL_SENDER = "Token not available"
        print("Token not available")
    GMAIL_USERNAME = SECRET_EMAIL_SENDER
    try:
        SECRET_EMAIL_SENDER_PW = os.environ["SECRET_EMAIL_SENDER_PW"]
    except KeyError:
        SECRET_EMAIL_SENDER_PW = "Token not available"
        print("Token not available")
    GMAIL_APP_PASSWORD = SECRET_EMAIL_SENDER_PW

    if update == 1: #Invio mail con il contenuto degli oggetti cambiati di prezzo
        changed_prices_path = 'changed_prices.txt'

        with open(changed_prices_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            file_content = ''.join(lines)

        if PRINT_DEBUG == True:
            print(file_content)

        if SEND_EMAIL == True:
            recipients = [SECRET_EMAIL_RECEIVER_1, SECRET_EMAIL_RECEIVER_2]
            msg = MIMEText(file_content)
            msg["Subject"] = "Prezzo degli articoli monitorati su amazon cambiato!!"
            msg["To"] = ", ".join(recipients)
            msg["From"] = f"{GMAIL_USERNAME}@gmail.com"
            smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            smtp_server.login(GMAIL_USERNAME, GMAIL_APP_PASSWORD)
            smtp_server.sendmail(msg["From"], recipients, msg.as_string())
            smtp_server.quit()