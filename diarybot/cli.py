"""GitDiaryBot command-line interface."""
import logging
from .bot import run_forever


def cli():
    """Start bot."""
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    run_forever()


if __name__ == '__main__':
    cli()
