from scrapy import Spider

from source.app.books.schemas import BookModel


class KitapYurduSpider(Spider):
    def __init__(self, db):
        self.db = db
        super().__init__()

    name = "kitapyurdu"
    start_urls = [
        "https://www.kitapyurdu.com/index.php?route=product/"
        "category&filter_category_all=true&path=1&filter_in_stock=1"
        "&filter_in_shelf=1&sort=p.sort_order&order=ASC&limit=100"
    ]

    async def parse(self, response):
        books = response.css(".product-cr")
        for book in books:
            if price := book.css("div.price-new span.value::text").get():
                price = price.strip()
            crawled_book = BookModel(
                title=book.css("div.name span::text").get(),
                publisher=book.css("div.publisher span::text").get(),
                writers=book.css("div.author span::text").getall(),
                price=price,
                url=book.css("div.name a::attr(href)").get(),
            ).model_dump()

            if not await self.db[self.name].find_one({"url": crawled_book.get("url")}):
                try:
                    await self.db[self.name].insert_one(crawled_book)
                except Exception:
                    pass
            elif book_url := crawled_book.get("url"):
                try:
                    await self.db[self.name].find_one_and_update(
                        {"url": book_url}, {"$set": crawled_book}
                    )
                except Exception:
                    pass

        if next_page := response.css(".pagination .next::attr(href)").get():
            yield response.follow(next_page, self.parse)
