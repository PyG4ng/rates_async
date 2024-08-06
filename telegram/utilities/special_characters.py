import re

CHARACTERS = [
    '[',
    ']',
    '(',
    ')',
    '~',
    '>',
    '#',
    '+',
    '-',
    '=',
    '|',
    '{',
    '}',
    '.',
    '!',
    '_',
    '*',
    '`',
]


def escape_all(text: str) -> str:
    for char in CHARACTERS:
        text = text.replace(char, rf'\{char}')
    return text


def frmt(num):
    return '{:,}'.format(num).replace(',', ' ')


def is_token_valid(token: str) -> bool:
    token_pattern = re.compile(r'^\$2a\$06\$[A-Za-z\d/.]{22}')
    return True if re.fullmatch(token_pattern, token) else False


if __name__ == '__main__':
    result = escape_all('bt_ut*y')
    print(result)
