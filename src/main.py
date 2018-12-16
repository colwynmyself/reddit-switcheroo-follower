from argparse import ArgumentParser

from src.config import config
from src.reddit import Reddit
from src.logger import logger
from src.models import Db, Link

MAX_DEPTH = 0


def get_links_from_comment(reddit, comment, depth=0):
    found_links = Reddit.get_links_from_comment(comment)

    if not found_links:
        logger.warning(
            f'No links were found in comment {comment.id}. Searching adjacent comments. Depth {depth}'
        )

        # search parent comment and child comments to n depth in case someone linked incorrectly
        # At depth > 0 we are searching child comments
        # At depth < 0 we are seatching parent comments
        # At depth 0 we are searching both directions
        # Max depth of 3 in any direction
        if abs(depth) > MAX_DEPTH:
            return found_links
        if depth <= 0:
            parent_comment = reddit.get_parent_comment(comment)
            if parent_comment:
                found_links.extend(
                    get_links_from_comment(reddit, parent_comment, (depth - 1)))
        if depth >= 0:
            child_comments = reddit.get_child_comments(comment)
            for child_comment in child_comments:
                child_links = get_links_from_comment(reddit, child_comment,
                                                     (depth + 1))
                if child_links:
                    found_links.extend(child_links)
                    break

    return found_links


def main(args):
    logger.setLevel(args.log_level.upper())

    db = Db()
    reddit = Reddit(
        client_id=config.client_id,
        client_secret=config.client_secret,
        user_agent=config.user_agent)

    switcheroo_links = []
    url = args.comment

    while True:
        comment = reddit.get_comment_from_url(url)
        found_links = get_links_from_comment(reddit, comment)

        if len(found_links) > 1:
            logger.info(
                f'Found {len(found_links)} links for {comment.id}. Using first.'
            )

        if not found_links:
            logger.warning(
                f'Oh no! No links were found in comment {comment.id}. Halting crawl.'
            )
            break

        link = found_links[0]
        switcheroo_links.append(link)
        url = link[1]
        logger.info(f'Following url {url}')

    logger.info(f'Found {len(switcheroo_links)} links')

    sess = db.create_session()

    depth = 0
    parent_link_id = None
    for text, link in switcheroo_links:
        depth += 1
        l = Link(
            url=link, text=text, depth=depth, parent_link_id=parent_link_id)
        sess.add(l)
        sess.flush()
        parent_link_id = l.id

    sess.commit()
    sess.close()


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
        '-l',
        '--log-level',
        help='Log level (default: warning)',
        dest='log_level',
        default='info',
        choices=['debug', 'info', 'warning', 'error', 'critical'],
    )
    args = parser.parse_args()
    main(args)
