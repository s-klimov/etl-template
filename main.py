import etl


def main():
    unloads = etl.load()
    multiplication = etl.transform(unloads)
    etl.extract(multiplication)


if __name__ == '__main__':
    main()
