from argparse import ArgumentParser

from src.switcheroo.config import config
from src.reddit import Reddit
from src.util.logger import logger


def sort_dict_items(item):
    return (item[1], item[0])


def main(args):
    logger.setLevel(args.log_level.upper())

    reddit = Reddit(
        client_id=config.client_id,
        client_secret=config.client_secret,
        user_agent=config.user_agent,
    )
    redditor = reddit.get_redditor(args.user)

    submissions = redditor.submissions.new(limit=None)

    submitted_subreddits = {}
    logger.info("Fetching submissions")
    submission_count = 0
    for submission in submissions:
        if submission_count % 100 == 0:
            logger.info(f"Fetched {submission_count} submissions")

        subreddit = submission.subreddit.display_name
        submitted_subreddits[subreddit] = submitted_subreddits.get(subreddit, 0) + 1

        submission_count += 1
    logger.info(f"Fetched {submission_count} submissions")

    comments = redditor.comments.new(limit=None)

    commented_subreddits = {}
    logger.info("Fetching comments")
    comment_count = 0
    for comment in comments:
        if comment_count % 100 == 0:
            logger.info(f"Fetched {comment_count} comments")

        subreddit = comment.subreddit.display_name
        commented_subreddits[subreddit] = commented_subreddits.get(subreddit, 0) + 1

        comment_count += 1
    logger.info(f"Fetched {comment_count} comments")

    print(sorted(submitted_subreddits.items(), key=sort_dict_items, reverse=True))
    print(sorted(commented_subreddits.items(), key=sort_dict_items, reverse=True))


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
