def p(body: object = None, synopsis: str = "", text: str = None):
    if synopsis:
        print(f"\033[31m{synopsis}:\033[0m")
    print(body, "\n")
    if text:
        print(f"\033[35m{text}\033[0m")

    print(f"\033[34m{'-' * 35}\033[0m")
