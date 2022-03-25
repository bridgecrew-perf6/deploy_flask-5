import re

ALPHA = re.compile(r"^[a-zA-Z0-9]*$")
ALPHA_SPACE = re.compile(r"^[a-zA-Z0-9 ]*$")
ALPHA_SPACE_SYMBOLS = re.compile(r"^[ A-Za-z0-9'_@./#&+-]*$")
DATE = re.compile(r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$")
EMAIL = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")