import enum


class RequestMethods(str, enum.Enum):
    get = "GET"
    post = "POST"
    delete = "DELETE"
    put = "PUT"


class ApiRoutes(str, enum.Enum):
    likes = "v1/likes"
    bookmarks = "v1/bookmarks"
    reviews = "v1/reviews"
