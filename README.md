# Book Scraper

---

### Requirements:

```
docker
docker-compose
```

### Run:

```
cp config/.env.example config/.env
docker-compose up --build -d
```

### Docs (Swagger UI):

```
localhost:8000/docs
```

### Endpoints:

```http request
POST   /books                     # crawl books
GET    /books                     # list books

GET    /                          # health check
```

### Example Requests/Responses:

#### Request:
```http request
POST /books

Headers:
Authorization: apikey

Body:
{
    "source": "kitapsepeti"
}
```


#### Response:
```json
{
    "detail": "Crawl started for source: kitapsepeti"
}
```


#### Request:
```http request
GET /books

Headers:
Authorization: apikey

Query Params:
source: str (kitapsepeti, kitapyurdu) Book source (required)
page: int Page number (optional)
size: int Items per page (optional)
sort: str (id, title) Sort by given value (optional)
order: str (asc, desc) Order by given value (optional)
```

#### Response:
```json
{
    "page": 1,
    "size": 3,
    "total": 11360,
    "pages": 3787,
    "books": [
        {
            "title": "Chainsaw Man 2",
            "publisher": "Gerekli Şeyler Yayıncılık",
            "writers": [
                "Tatsuki Fujimoto"
            ],
            "price": "60,48",
            "url": "https://www.kitapsepeti.com/chainsaw-man-2"
        },
        {
            "title": "Kürk Mantolu Madonna",
            "publisher": "Yapı Kredi Yayınları",
            "writers": [
                "Sabahattin Ali"
            ],
            "price": "16,75",
            "url": "https://www.kitapsepeti.com/kurk-mantolu-madonna-126934"
        },
        {
            "title": "Orion Ciltli",
            "publisher": "Martı Yayınları",
            "writers": [
                "Almina Taner"
            ],
            "price": "112,50",
            "url": "https://www.kitapsepeti.com/orion-ciltli"
        }
    ]
}
```

### Scheduled Tasks:

```
crawl_kitapsepeti: works every day at 00.00
crawl_kitapyurdu: works every day at 01.00
```
---
