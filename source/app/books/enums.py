from enum import Enum


class Source(str, Enum):
    KITAPSEPETI = "kitapsepeti"
    KITAPYURDU = "kitapyurdu"


class Sort(str, Enum):
    ID = "id"
    TITLE = "title"


class Order(str, Enum):
    ASC = "asc"
    DESC = "desc"
