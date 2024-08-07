from utils import opentdb_questions_utils
from utils import trivia_questions_utils
from utils import quiz_questions_utils


def main():
    opentdb_questions_utils.get_and_store_questions()
    opentdb_questions_utils.get_and_store_categories()
    trivia_questions_utils.get_and_store_questions_and_categories()
    quiz_questions_utils.get_and_store_questions_and_categories()

if __name__ == '__main__':
    main()
