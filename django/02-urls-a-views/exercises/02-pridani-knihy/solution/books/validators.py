import datetime


def validate_required(data, name, required=True):
    present = name in data
    error_message = None

    if required and not present:
        error_message = "Povinne pole"

    return error_message, present


def validate_year(data, required=True):
    error_message, field_present = validate_required(data, "year", required)
    if error_message:
        return error_message

    if not field_present:
        return None

    value = data["year"]

    if isinstance(value, bool) or not isinstance(value, int):
        return "Musí být celé číslo"

    if value > datetime.datetime.now().year:
        return "Rok nesmí být v budoucnosti"

    return None


def validate_author(data, required=True):
    error_message, field_present = validate_required(data, "author", required)
    if error_message:
        return error_message

    if not field_present:
        return None

    value = data["author"]

    if not isinstance(value, str) or len(value.strip()) == 0:
        return "Musi byt neprazdny text"

    return None


def validate_title(data, required=True):
    error_message, field_present = validate_required(data, "title", required)
    if error_message:
        return error_message

    if not field_present:
        return None

    value = data["title"]

    if not isinstance(value, str) or len(value.strip()) == 0:
        return "Musi byt neprazdny text"

    return None


def validate_data(data, required=True):
    error_fields = {
        field: error_message
        for field, error_message in [
            ("author", validate_author(data, required=required)),
            ("title", validate_title(data, required=required)),
            ("year", validate_year(data, required=required)),
        ]
        if error_message
    }

    return error_fields
