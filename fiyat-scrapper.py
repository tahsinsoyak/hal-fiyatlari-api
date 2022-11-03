from unicodedata import name
import pandas as pd
from bs4 import BeautifulSoup
import requests
import json
import os

def _scrape_veri():
    url='https://www.antalya.bel.tr/BilgiEdin/halden-gunluk-fiyatlar'
    response = requests.get(url)


    isimler = []
    fiyatlar = []
    birimler = []
    #print(response.status_code)

    html_content = response.content
    html_content_string = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    container_div = soup.findAll('div', class_='market-place-item')

    for i in container_div:
        isim = i.findAll('div', class_='market-place-item-name')
        for j in isim:
            p = j.findAll('p')
            for t in p:
                ürünismi = t.get_text()
                isimler.append(ürünismi)
        fiyat = i.findAll('div', class_='market-place-pricing-wrap')
        for j in fiyat:
            p = j.findAll('p')
            for t in p:
                ürünismi = t.get_text()
                fiyatlar.append(ürünismi)
        birim = i.findAll('div', class_='market-place-unit')
        for j in birim:
            p = j.findAll('p')
            for t in p:
                birim = t.get_text().strip()
                birimler.append(birim)


    #fiyat ayirma
    eyf = []
    edf = []


    for i in range(0,len(fiyatlar)-6):
        if i % 2 == 0:
            edf.append(fiyatlar[i])
        else:
            eyf.append(fiyatlar[i])

    isimler = isimler[0:len(isimler)-6]

    #print(len(isimler),len(edf),len(eyf),len(birimler))

    df = pd.DataFrame({'urunismi': isimler,
                        'edf': edf,
                        'eyf': eyf,
                        'birim':birimler
                        })

    #print(df)
    return df


def _kaydet():
    df = _scrape_veri()
    result = df.to_json(orient="records")
    with open(f"src/ant_veriler.json","w") as file:
        file.write(result)


if __name__ == "__main__":
    _kaydet()