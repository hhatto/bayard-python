from bayard import BayardHTTPClient


def main():
    c = BayardHTTPClient(port=8088)
    print(c.status())
    print(c.schema())
    print(c.get_document("100"))


if __name__ == "__main__":
    main()
