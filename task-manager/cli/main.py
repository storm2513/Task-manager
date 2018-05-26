from cli.arg_parser import *
from config.commands import *
from config.session import *


def run():
    start_session()
    process_args()


if(__name__ == "__main__"):
    run()
