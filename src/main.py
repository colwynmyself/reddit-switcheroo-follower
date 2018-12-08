from argparse import ArgumentParser
from time import sleep

from src.config import Config
from src.io import write_links_to_csv
from src.reddit import Reddit
from src.logger import logger


def main(args):
    config = Config('development')
    reddit = Reddit(
        client_id=config.client_id,
        client_secret=config.client_secret,
        user_agent=config.user_agent)
    logger.setLevel(args.log_level.upper())

    switcheroo_links = []
    url = args.comment

    while True:
        found_links = reddit.get_links_from_comment_url(url)
        if not len(found_links):
            logger.warning(f'Oh no! No links were found in comment {url}')
            # search parent comment and child comments to n depth in case someone linked incorrectly
            break

        if len(found_links) > 1:
            logger.info(f'Found {len(found_links)} links for {url}. Using first.')

        link = found_links[0]
        switcheroo_links.append(link)
        url = link[1]
        logger.info(f'Following url {url}')

    logger.info(f'Found {len(switcheroo_links)} links')
    write_links_to_csv(args.output, switcheroo_links)


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument(
        '-c',
        '--comment',
        help='Comment to start the hole at',
        dest='comment',
        required=True,
    )
    parser.add_argument(
        '-o',
        '--output',
        help='CSV to output data into',
        dest='output',
        required=True,
    )
    parser.add_argument(
        '-l', '--log-level',
        help='Log level (default: warning)',
        dest='log_level',
        default='info',
        choices=['debug', 'info', 'warning', 'error', 'critical'],
    )
    args = parser.parse_args()
    main(args)
