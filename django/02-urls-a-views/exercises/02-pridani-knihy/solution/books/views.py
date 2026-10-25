from http import HTTPStatus

from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from books.data.books import BOOKS
from books.utils import (
    ReadableJsonResponse,
    find_book,
    load_data_from_request,
    serialize_book,
)
from books.validators import validate_data


@csrf_exempt
@require_http_methods(["GET", "POST"])
def book_list(request):
    if request.method == "GET":
        results = list(map(lambda book: serialize_book(book, request=request), BOOKS))
        return ReadableJsonResponse(
            {"count": len(results), "results": results}, status=HTTPStatus.OK
        )

    # POST

    data, error_response = load_data_from_request(request)

    if error_response:
        return error_response

    error_fields = validate_data(data)

    if error_fields:
        return ReadableJsonResponse(
            {
                "errors": error_fields,
            },
            status=HTTPStatus.BAD_REQUEST,
        )

    book_raw = {
        "id": max(map(lambda book: book["id"], BOOKS), default=0) + 1,
        "title": data["title"].strip(),
        "year": data["year"],
        "author": data["author"].strip(),
    }

    BOOKS.append(book_raw)

    book = serialize_book(
        book_raw,
        request=request,
    )

    response = ReadableJsonResponse(book, status=HTTPStatus.CREATED)
    response.headers["Location"] = book.get("url")

    return response


@csrf_exempt
@require_http_methods(["GET", "DELETE"])
def book_detail(request, book_id: int):
    book, book_index = find_book(book_id)

    if book is None:
        return ReadableJsonResponse(
            {"error": "Kniha nenalezena"}, status=HTTPStatus.NOT_FOUND
        )

    # GET
    if request.method == "GET":
        return ReadableJsonResponse(
            serialize_book(book, request=request), status=HTTPStatus.OK
        )

    BOOKS.pop(book_index)

    return HttpResponse(status=HTTPStatus.NO_CONTENT)
