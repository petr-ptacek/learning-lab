from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from books.views import (
    ReadableJsonResponse,
    clean_book_fields,
    find_book,
    parse_json_object,
    serialize_book,
    validate_book,
)


# csrf_exempt: stejný důvod jako v books/views.py.
@csrf_exempt
@require_http_methods(["GET", "PATCH"])
def book_detail(request, book_id):
    book = find_book(book_id)
    if book is None:
        return ReadableJsonResponse({"error": "Kniha nenalezena"}, status=404)
    if request.method == "GET":
        return ReadableJsonResponse(serialize_book(book))

    data, error_response = parse_json_object(request)
    if error_response:
        return error_response
    errors = validate_book(data, partial=True)
    if errors:
        return ReadableJsonResponse({"errors": errors}, status=400)

    book.update(clean_book_fields(data))
    return ReadableJsonResponse(serialize_book(book))
