def is_email(validate_str):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email(validate_str)
        return True
    except ValidationError:
        return False


def is_md5(validate_str):
    import re
    return re.match(r'(?i)(?<![a-z0-9])[a-f0-9]{32}(?![a-z0-9])', validate_str)


def string_to_md5(orig_str):
    import hashlib
    hash_object = hashlib.md5(orig_str)
    return hash_object.hexdigest()


def validate_key(key):
    # TODO: Complete this function:
    return key


def clean_key(dirty_key):
    return dirty_key.decode('utf-8').lower()
