from utils.opentdb_questions_utils import get_and_store_questions, get_and_store_categories
from utils.trivia_questions_utils import get_and_store_questions_and_categories


def main():
    get_and_store_questions()
    get_and_store_categories()
    get_and_store_questions_and_categories()

if __name__ == '__main__':
    main()
