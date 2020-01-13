"""GitDiaryBot command-line interface."""
import sys
import logging

from .bot import run_forever


def cli():
    """Start bot."""
    if sys.argv and sys.argv[-1] == "debug":
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=log_level,
    )
    run_forever()


if __name__ == '__main__':
    cli()
