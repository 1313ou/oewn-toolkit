import process


def test_process_wn_quotes(s):
    p = process.process_wn_quotes(s)
    print(f" -> {p}")
    return p


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
