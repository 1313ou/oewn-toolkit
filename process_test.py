import process


def test_escape_apostrophe(s):
    p = process.escape_apostrophe(s)
    print(p)


def test_process_wn_quotes(s):
    p = process.process_wn_quotes(s)
    print(f" -> {p}")
    return p


def main2():
    test_escape_apostrophe("General officers' caps are similar to those of field-grade officers, but the cap band is dark blue and embroidered with gold oak leaf motifs.")
    test_escape_apostrophe("He's gone.")
    test_escape_apostrophe("`He' refers to a person.")
    test_escape_apostrophe("`Stalin's mustache' refers to Stalin's mustache.")
    test_escape_apostrophe("`The others' fate' is an expression.")

def main():
    r = test_process_wn_quotes("   `a'      `b'      `c'   ")
    print(r)
    r = test_process_wn_quotes("   `abc'      `def'      `ghi'   ")
    print(r)
    r = test_process_wn_quotes("`a'`b'`c'")
    print(r)
    r = test_process_wn_quotes("`'")
    print(r)


if __name__ == '__main__':
    main()
