from argparse import ArgumentParser

from src.switcheroo.config import config
from src.reddit import Reddit
from src.util.logger import logger


def main(args):
    logger.setLevel(args.log_level.upper())

    reddit = Reddit(
        client_id=config.client_id,
        client_secret=config.client_secret,
        user_agent=config.user_agent,
    )
    redditor = reddit.get_redditor(args.user)

    submissions = redditor.submissions.new(limit=None)

    total_submissions = 0
    for submission in submissions:
        total_submissions += 1
        print(submission.title)
        print(f"https://www.reddit.com{submission.permalink}")
        print(submission.url)
        print("-----------\n")

    print("--------- COMMENTS -----------")
    comments = redditor.comments.new(limit=None)

    total_comments = 0
    for comment in comments:
        total_comments += 1
        print(comment.body)
        print(f"https://www.reddit.com{comment.permalink}")
        print("-----------\n")

    print(total_submissions)
    print(total_comments)


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument(
        "-u", "--username", help="User to get details of", dest="user", required=True
    )
    parser.add_argument(
        "-l",
        "--log-level",
        help="Log level (default: warning)",
        dest="log_level",
        default="info",
        choices=["debug", "info", "warning", "error", "critical"],
    )
    args = parser.parse_args()
    main(args)
