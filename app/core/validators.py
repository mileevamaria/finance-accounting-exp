from pydantic import EmailStr, TypeAdapter, ValidationError


def is_identifier_email(value: str) -> bool:
    email_adapter = TypeAdapter(EmailStr)
    try:
        email_adapter.validate_python(value)
        return True
    except ValidationError:
        return False
