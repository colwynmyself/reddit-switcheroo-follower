import re
import praw
from praw.models import Comment

from src.reddit.decorators import RequestDecorator

request_decorator = RequestDecorator()

class Reddit:
    """
    Reddit class to handle higher level reddit actions.

    Requests are rate limited to 1 request/second
    """
    def __init__(self, *args, **kwargs):
        self._reddit = praw.Reddit(**kwargs)


    @request_decorator.make_request
    def get_links_from_comment_url(self, url):
        comment = Comment(self._reddit, url=url)
        text = comment.body
        return self._parse_links(text)


    @request_decorator.make_request
    def get_links_from_comment_id(self, id):
        comment = Comment(self._reddit, id=id)
        text = comment.body
        return self._parse_links(text)


    def _parse_links(self, comment):
        """
        Given the text of a reddit comment, finds all links with format [text](link)
        """
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
