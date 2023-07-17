from scrapy import Spider

from source.app.books.schemas import BookModel


class KitapSepetiSpider(Spider):
    def __init__(self, db):
        self.db = db
        super().__init__()

    name = "kitapsepeti"
    url = "https://www.kitapsepeti.com"
    start_urls = [
        f"{url}/roman?stock=1",
        f"{url}/cocuk-kitaplari?stock=1",
        f"{url}/cizgi-roman?stock=1",
        f"{url}/sinavlara-hazirlik-kitaplari?stock=1",
        f"{url}/bilimkurgu?stock=1",
        f"{url}/turk-edebiyati?stock=1",
    ]

    async def parse(self, response):
        books = response.css("div.col.col-12.drop-down.hover.lightBg")
        for book in books:
            if price := book.css(
                "div.fl.col-12.tooltipWrapper "
                "div.fl.col-12.d-flex.productPrice "
                "div.fl.col-12.priceWrapper "
                "div.col.col-12.currentPrice::text"
            ).get():
                price = price.strip().split("\n")[0]
            crawled_book = BookModel(
                title=book.css(".detailLink::attr(title)").get(),
                publisher=book.css("a.col.col-12.text-title.mt::text").get(),
                writers=book.css("#productModelText::text").getall(),
                price=price,
                url=f'{self.url}{book.css(".detailLink::attr(href)").get()}',
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

        if next_page := response.css(".next::attr(href)").get():
            return response.follow(f"{self.url}{next_page}", self.parse)
