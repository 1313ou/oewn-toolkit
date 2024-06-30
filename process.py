import re
import sys

#  H E L P E R S

# old scheme:
# `quoted'
#
# new scheme:
# `quoted´
#
# new scheme2:
# “quoted”

APOS_SUB = '###'
LEFT_QUOTE_SUB = '<<<'
RIGHT_QUOTE_SUB = '>>>'
QUOTES = "‘’‛‚“”‟„❛❜❝❞❟❠«»"


# A P O S T R O P H E

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


# U N E V E N / U N C L O S E D

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


# F I N D

def search_using_find(input_text, what):
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


def find_regex(input_text, regex):
    if search_regex(input_text, regex):
        return input_text
    return None


def find_pair(input_text, b1, b2):
    r = search_regex(input_text, fr'{b1}[^{b2}]*{b2}')
    if r:
        return r
    return None


def find_one_of(input_text, list):
    r = search_regex(input_text, fr'[{list}]')
    if r:
        return r
    return None


# S U B S T I T U T I O N


def search_sub(input_text, regex, replacement):
    if re.search(regex, input_text):
        return re.sub(regex, replacement, input_text)
    return None


# M A R K


def mark_apostrophe(input_text):
    esc = escape_apostrophe(input_text)
    return f"{esc}" if esc != input_text else None


def mark_wn_quotes(input_text):
    regex = r"`([^´]*)´"
    replacement = f"{LEFT_QUOTE_SUB}\\1{RIGHT_QUOTE_SUB}"
    if re.search(regex, input_text):
        return re.sub(regex, replacement, input_text)
    return None


#  C A L L A B L E

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


def find_uneven_apostrophes(input_text):
    return uneven(input_text, '\'')


def find_unclosed_wn_quotes(input_text):
    return unclosed(input_text, '`', '´')


def find_unclosed_wn_quotes_excluding_apostrophe(input_text):
    esc = escape_apostrophe(input_text)
    return find_unclosed_wn_quotes(esc)


def find_semicolon_after_space(input_text):
    return search_regex(input_text, r' ;')


def find_comma_after_space(input_text):
    return search_regex(input_text, r' ,')


def find_stop_after_space(input_text):
    return search_regex(input_text, r' \.')


def find_2_hyphens(input_text):
    return find_regex(input_text, r'--')


def find_double_quotes(input_text):
    return search_regex(input_text, r'"')


def find_backtick(input_text):
    return find_regex(input_text, r'`')


def find_expanding_apostrophe(input_text):
    return find_regex(input_text, r'＇')


def find_angle_brackets(input_text):
    return find_pair(input_text, r'\[', r']')


def find_diamond_brackets(input_text):
    return find_pair(input_text, '<', '>')


def find_wn_quotes(input_text):
    return find_pair(input_text, '`', "'")


def find_new_x_quotes(input_text):
    return find_pair(input_text, '“', '”')


def find_new_x_quote1(input_text):
    return find_regex(input_text, r'“')


def find_new_x_quote2(input_text):
    return find_regex(input_text, r'”')

dialog_tags='ask|enquire|question'
dialog_tags='say|said|tell|told|add|continue|reply|replied|answer|exclaim|explain|declare|interpose|cut in|comment|repeat|shout|chorus|shrug|nod'

def find_dialog_tags(input_text):
    return find_regex(input_text, rf'`[^´]*´.*({dialog_tags})')


def find_oddities(input_text):
    # if find_wn_quotes(input_text):
    #     return f"wnq\t{input_text}"
    # if find_uneven_apostrophes(input_text):
    #    return f"a3\t{input_text}"

    if find_unclosed_wn_quotes(input_text):
        return f"`?\t{input_text}"
    if find_unclosed_parentheses(input_text):
        return f"(?\t{input_text}"

    if find_uneven_double_quotes(input_text):
        return f'"""\t{input_text}'

    if find_2_hyphens(input_text):
        return f"--\t{input_text}"
    # if find_backtick(input_text):
    #    return f"bt\t{input_text}"

    if find_etc(input_text):
        return f"etc\t{input_text}"
    if find_eg(input_text):
        return f"eg\t{input_text}"
    if find_eg(input_text):
        return f"ie\t{input_text}"

    if find_double_quotes(input_text):
        return f'"\t{input_text}'

    if find_angle_brackets(input_text):
        return f"[]\t{input_text}"
    if find_diamond_brackets(input_text):
        return f"<>\t{input_text}"

    if find_semicolon_after_space(input_text):
        return f"sp;\t{input_text}"
    if find_comma_after_space(input_text):
        return f"sp,\t{input_text}"
    if find_stop_after_space(input_text):
        return f"sp.\t{input_text}"

    if find_expanding_apostrophe(input_text):
        return f"ea\t{input_text}"
    if find_new_x_quotes(input_text):
        return f"xq\t{input_text}"
    if find_new_x_quote1(input_text):
        return f"xq1\t{input_text}"
    if find_new_x_quote2(input_text):
        return f"xq2\t{input_text}"

    if find_one_of(input_text, QUOTES):
        return f"qq\t{input_text}"

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


def process_2_hyphens(input_text):
    r = r'\s*--\s*'
    s = " — "
    return search_sub(input_text, r, s)


def default_process(input_text):
    return input_text
