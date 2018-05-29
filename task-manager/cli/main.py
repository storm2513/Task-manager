from cli.arg_parser import *
from lib.config.commands import *
from lib.config.session import *


def run():
    start_session()
    process_args()


if(__name__ == "__main__"):
    run()
