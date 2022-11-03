import fastapi as _fastapi
import json
from typing import Optional
from fastapi import Query

app = _fastapi.FastAPI()


with open('ant_veriler.json','r') as f:
    urunler = json.load(f)

@app.get("/")
def root():
    return {"message": "hosgeldiniz"}


#tüm ürünler ve arama için
@app.get('/search',status_code=200)
def search_urun(name: Optional[str] = Query(None, title="Name",description="Aranacak Ürün Giriniz.")):
    if name is None:
        return urunler
    else:
        people2 = [p for p in urunler if name.lower() in p ['urunismi'].lower()]
        return people2


#http://127.0.0.1:8000/search?name=cilek /isme göre arama

#http://127.0.0.1:8000/search    /tüm verinin bulunduğu