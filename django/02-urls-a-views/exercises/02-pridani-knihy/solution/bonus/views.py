from http import HTTPStatus

from django.http.request import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from books import views as book_views
from books.utils import (
    ReadableJsonResponse,
    find_book,
    load_data_from_request,
    serialize_book,
)
from books.validators import validate_data


@csrf_exempt
@require_http_methods(["PATCH", "GET"])
def book_detail(request: HttpRequest, book_id):
    if request.method == "GET":
        return book_views.book_detail(request, book_id)

    book, book_index = find_book(book_id)

    if book is None:
        return ReadableJsonResponse(
            {"error": "Kniha nenalezena"}, status=HTTPStatus.NOT_FOUND
        )

    data, error_response = load_data_from_request(request)
    if error_response:
        return error_response

    error_fields = validate_data(data, required=False)
    if error_fields:
        return ReadableJsonResponse(
            {
                "errors": error_fields,
            },
            status=HTTPStatus.BAD_REQUEST,
        )

    book.update(
        {
            "title": data.get("title", book["title"]).strip(),
            "author": data.get("author", book["author"]).strip(),
            "year": data.get("year", book["year"]),
        }
    )

    return ReadableJsonResponse(
        serialize_book(book, request=request), status=HTTPStatus.OK
    )
