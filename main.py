from assets import extractor
from assets import sqlCreator

def main():
    sqlCreator.create_table()
    extractor.emnist_to_sql()


if __name__ == '__main__':
    main()