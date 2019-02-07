from argparse import ArgumentParser

from src.switcheroo.config import config
from src.reddit import Reddit
from src.util.logger import logger
from src.db import Db
from src.db.models import Comment, User, Submission, Subreddit


def sort_dict_items(item):
    return (item[1], item[0])


def upsert_subreddit(session, sub):
    subreddit = (
        session.query(Subreddit).filter(Subreddit.reddit_id == sub.id).one_or_none()
    )
    if not subreddit:
        subreddit = Subreddit(reddit_id=sub.id, name=sub.display_name)
        session.add(subreddit)
        session.flush()

    return subreddit


def upsert_submission(session, subreddit, user, s):
    submission = (
        session.query(Submission).filter(Submission.reddit_id == s.id).one_or_none()
    )
    if not submission:
        submission = Submission(
            reddit_id=s.id,
            title=s.title,
            text=s.selftext,
            permalink=s.permalink,
            url=s.url,
            author_id=user.id,
            subreddit_id=subreddit.id,
        )
        session.add(submission)
        session.flush()

    return submission


def upsert_comment(session, subreddit, user, submission, comment):
    c = session.query(Comment).filter(Comment.reddit_id == comment.id).one_or_none()
    if not c:
        c = Comment(
            reddit_id=comment.id,
            body=comment.body,
            permalink=comment.permalink,
            submission_id=submission.id,
            author_id=user.id,
            subreddit_id=subreddit.id,
        )
        session.add(c)
    return c


def upsert_redditor(session, redditor):
    user = session.query(User).filter(User.reddit_id == redditor.id).one_or_none()
    if not user:
        user = User(reddit_id=redditor.id, username=redditor.name)
        session.add(user)
        session.flush()
    return user


def main(args):
    logger.setLevel(args.log_level.upper())

    reddit = Reddit(
        client_id=config.client_id,
        client_secret=config.client_secret,
        user_agent=config.user_agent,
    )
    db = Db()
    session = db.create_session()

    redditor = reddit.get_redditor(args.user)
    user = upsert_redditor(session, redditor)

    seen_subreddits = {}
    submissions = redditor.submissions.new(limit=None)
    submission_count = 0
    for submission in submissions:
        if submission_count % 100 == 0:
            print(f"Finished {submission_count} submissions")
            session.commit()
        submission_count += 1
        sub = submission.subreddit

        # Check cache
        subreddit = seen_subreddits.get(sub.id)
        if not subreddit:
            subreddit = upsert_subreddit(session, sub)
            seen_subreddits[sub.id] = subreddit

        upsert_submission(session, subreddit, user, submission)
    print(f"{submission_count} total submissoins")

    comments = redditor.comments.new(limit=None)
    comment_count = 0
    for comment in comments:
        if comment_count % 100 == 0:
            print(f"Finished {comment_count} comments")
            session.commit()
        comment_count += 1
        sub = comment.subreddit

        # Check cache
        subreddit = seen_subreddits.get(sub.id)
        if not subreddit:
            subreddit = upsert_subreddit(session, sub)
            seen_subreddits[sub.id] = subreddit

        submission = upsert_submission(session, subreddit, user, comment.submission)

        upsert_comment(session, subreddit, user, submission, comment)
    print(f"{comment_count} total comments")

    session.commit()
    session.close()


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
