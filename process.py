import re
import sys

#  H E L P E R S

APOS_SUB = '###'
LEFT_QUOTE_SUB = '<<<'
RIGHT_QUOTE_SUB = '>>>'


def unescape_apostrophe(input_text):
    return re.sub(rf'{APOS_SUB}', r'\'', input_text)


# this does not handle Socrates'.others' genitives
def escape_apostrophe(input_text):
    esc = input_text
    esc = re.sub(r'(\S)\'s\b', f'\\1{APOS_SUB}s', esc)
    esc = re.sub(r'(\S)\'re\b', f'\\1{APOS_SUB}re', esc)
    esc = re.sub(r'(\S)\'ve\b', f'\\1{APOS_SUB}ve', esc)
    esc = re.sub(r'(\S)\'d\b', f'\\1{APOS_SUB}d', esc)
    esc = re.sub(r'(\S)\'ll\b', f'\\1{APOS_SUB}ll', esc)
    esc = re.sub(r'(\S)\'m\b', f'\\1{APOS_SUB}m', esc)
    esc = re.sub(r'n\'t\b', f'n{APOS_SUB}t', esc)
    esc = re.sub(r'\'tis\b', f'{APOS_SUB}tis', esc)
    esc = re.sub(r'o\'clock\b', f'o{APOS_SUB}clock', esc)
    return esc


def escape_apostrophe_auto(input_text):
    esc = escape_apostrophe(input_text)

    xesc = esc
    for w in ('students', 'opponents', 'florists', 'parents', 'neighbors', 'Years', 'Saints'):
        xesc = re.sub(fr'({w})\'(\s)', f'\\1{APOS_SUB}\\2', xesc)  # plural genitive

    xesc = re.sub(r'maitre d\'(\s)', f'maitre d{APOS_SUB}\\1', xesc)  # maitre d'
    xesc = re.sub(r'(\s)d\'(\S)', f'\\1d{APOS_SUB}\\2', xesc)  # maitre d'
    xesc = re.sub(r'd\'etat', f'd{APOS_SUB}etat', xesc)  # coup d'etat
    xesc = re.sub(r'd\'Unite', f'd{APOS_SUB}Unite', xesc)  # d'Unite

    xesc = re.sub(r'\bO\'\b', f'O{APOS_SUB}', xesc)  # maitre d'
    if xesc != esc:
        print(xesc, file=sys.stderr)
    return xesc


def uneven(input_text, c):
    collected = [m.start() for m in re.finditer(rf'{c}', input_text)]
    if len(collected) % 2 != 0:
        return collected[-1]
    else:
        return None


def unclosed(input_text, left, right):
    pat = rf'[{left}{right}]'
    # Find all left and right marks in the text
    marks = [m.group() for m in re.finditer(pat, input_text)]

    # Stack to track unclosed parentheses
    stack = []
    for mark in marks:
        if mark == left:
            stack.append(mark)
        elif mark == right:
            if stack and stack[-1] == left:
                stack.pop()
            else:
                # An unmatched closing mark found
                return input_text.index(mark)

    # If stack is not empty, there are unclosed opening marks
    if stack:
        return input_text.rindex(left)
    else:
        return None


def find_using_find(input_text, what):
    if input_text.find(what) != -1:
        return True
    return None


def search_str(input_text, what):
    return search_regex(input_text, fr"{what}")


def search_regex(input_text, regex):
    match = re.search(regex, input_text)
    if match:
        return match.group()
    else:
        return None


def search_sub(input_text, regex, replacement):
    if re.search(regex, input_text):
        return re.sub(regex, replacement, input_text)
    return None


def set_apostrophe_escape(input_text):
    esc = escape_apostrophe(input_text)
    return f"{esc}" if esc != input_text else None


def sub_wn_quotes(input_text):
    regex = r"`([^']*)'"
    replacement = f"{LEFT_QUOTE_SUB}\\1{RIGHT_QUOTE_SUB}"
    if re.search(regex, input_text):
        return re.sub(regex, replacement, input_text)
    return None


#  C A L L A B L E

def find_2_hyphens(input_text):
    return search_str(input_text, '--')


def find_emdash_if_has_2_hyphens(input_text):
    r = r'\s*--\s*'
    s = " —— "
    return search_sub(input_text, r, s)


def find_etc(input_text):
    r = r'\betc([^\.a-z])'
    s = "etc.\\1"
    return search_sub(input_text, r, s)


def find_eg(input_text):
    r = r'\beg\b'
    s = "e.g."
    return search_sub(input_text, r, s)


def find_ie(input_text):
    r = r'\bie\b'
    s = "i.e."
    return search_sub(input_text, r, s)


def find_unclosed_parentheses(input_text):
    return unclosed(input_text, '(', ')')


def find_uneven_double_quotes(input_text):
    return uneven(input_text, '"')


def find_uneven_single_quotes(input_text):
    return uneven(input_text, '\'')


def find_unclosed_wn_quotes(input_text):
    return unclosed(input_text, '`', '\'')


def find_unclosed_wn_quotes_excluding_apostrophe(input_text):
    esc = escape_apostrophe(input_text)
    return find_unclosed_wn_quotes(esc)


def find_semicolon_after_space(input_text):
    return search_regex(input_text, r' ;')


def find_double_quotes(input_text):
    return search_regex(input_text, r'"')


def find_backtick(input_text):
    return search_regex(input_text, r'`')


def find_expanding_apostrophe(input_text):
    if search_regex(input_text, r'＇'):
        return input_text
    return None


def find_brackets(input_text, b1, b2):
    r = search_regex(input_text, fr'{b1}[^{b2}]*{b2}')
    if r:
        return r
    return None


def find_angle_brackets(input_text):
    return find_brackets(input_text, '<', '>')


def find_wn_quotes(input_text):
    return find_brackets(input_text, '<', '>')
    # return search_regex(input_text, r"`.*'")


def find_new_quotes(input_text):
    return find_brackets(input_text, '“', '”')


def find_oddities(input_text):
    if find_wn_quotes(input_text):
        return input_text
    if find_double_quotes(input_text):
        return input_text

    if find_unclosed_wn_quotes(input_text):
        return input_text
    if find_unclosed_parentheses(input_text):
        return input_text

    if find_uneven_double_quotes(input_text):
        return input_text
    if find_uneven_single_quotes(input_text):
        return input_text

    if find_2_hyphens(input_text):
        return input_text
    if find_backtick(input_text):
        return input_text

    if find_etc(input_text):
        return input_text
    if find_eg(input_text):
        return input_text

    if find_angle_brackets(input_text):
        return input_text
    return None


def process_apostrophe_1(input_text):
    r = find_unclosed_wn_quotes(input_text)
    if r:
        return input_text
    return None


def process_escape_apostrophe_auto(input_text):
    esc = escape_apostrophe(input_text)
    if find_unclosed_wn_quotes(input_text):
        esc = process_escape_apostrophe_auto(input_text)
    return esc


def process_wn_quotes(input_text):
    r = sub_wn_quotes(input_text)
    if r:
        return r
    return input_text


def default_process(input_text):
    return input_text
