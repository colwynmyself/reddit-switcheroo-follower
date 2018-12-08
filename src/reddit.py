import praw
from praw.models import Comment

from argparse import ArgumentParser

from src.config import Config


def main(args):
    config = Config('development')
    reddit = praw.Reddit(
        client_id=config.client_id,
        client_secret=config.client_secret,
        user_agent=config.user_agent)

    comment = Comment(reddit, url=args.comment)
    print(comment.body)


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument(
        '-c', '--comment',
        help='Comment to start the hole at',
        dest='comment',
        required=True,
    )
    args = parser.parse_args()
    main(args)