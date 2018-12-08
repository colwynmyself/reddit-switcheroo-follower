import praw
from praw.models import Comment

import re
from argparse import ArgumentParser
from time import sleep

from src.config import Config


def parse_links(comment):
    link_regex = r'\[([^\]]+)\]\s?\(([^\)]+)\)'
    matches = re.finditer(link_regex, comment)

    links = []
    for match in matches:
        try:
            text = match.group(1).strip()
            link = match.group(2).strip()
            links.append((text, link))
        except:
            pass

    return links


def get_links_from_comment_url(reddit, url):
    comment = Comment(reddit, url=url)
    text = comment.body
    return parse_links(text)


def write_links_to_csv(csv, links):
    with open(csv, 'w+') as f:
        depth = 0
        for text, link in links:
            f.write(f'{text},{link},{depth}\n')
            depth += 1


def main(args):
    config = Config('development')
    reddit = praw.Reddit(
        client_id=config.client_id,
        client_secret=config.client_secret,
        user_agent=config.user_agent)

    links_so_far = []
    url = args.comment

    while True:
        found_links = get_links_from_comment_url(reddit, url)
        if not len(found_links):
            print(f'Oh no! No links were found in comment {url}')
            break

        if len(found_links) > 1:
            print(f'Found {len(found_links)} links for {url}. Using first.')

        link = found_links[0]
        links_so_far.append(link)
        url = link[1]
        print(f'Following url {url}')
        # don't get rate limited, friends
        sleep(1)

    print(f'Found {len(links_so_far)} links')
    write_links_to_csv(args.output, links_so_far)


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
    args = parser.parse_args()
    main(args)