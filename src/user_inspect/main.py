from argparse import ArgumentParser

from src.switcheroo.config import config
from src.reddit import Reddit
from src.util.logger import logger


def main(args):
    logger.setLevel(args.log_level.upper())

    reddit = Reddit(
        client_id=config.client_id,
        client_secret=config.client_secret,
        user_agent=config.user_agent)
    redditor = reddit.get_redditor(args.user)
    all_submissions = []

    submissions = redditor.submissions.new()
    while True:
        all_submissions.extend(submissions)

        try:
            submissions = next(submissions)
        except StopIteration:
            break

    for submission in all_submissions:
        print('\n-----------\n')
        print(submission.title)
        print(f'https://www.reddit.com{submission.permalink}')
        print(submission.url)


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument(
        '-u',
        '--username',
        help='User to get details of',
        dest='user',
        required=True,
    )
    parser.add_argument(
        '-l',
        '--log-level',
        help='Log level (default: warning)',
        dest='log_level',
        default='info',
        choices=['debug', 'info', 'warning', 'error', 'critical'],
    )
    args = parser.parse_args()
    main(args)
