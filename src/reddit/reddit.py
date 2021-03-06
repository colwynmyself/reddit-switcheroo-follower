import re
import praw
from praw.models import Comment, Redditor
from src.reddit.decorators import RequestDecorator

request_decorator = RequestDecorator()


class Reddit:
    """
    Reddit class to handle higher level reddit actions.

    Requests are rate limited to 1 request/second
    """
    _link_regex = r'\[([^\]]+)\]\s?\(([^\)]+)\)'

    def __init__(self, *args, **kwargs):
        self._reddit = praw.Reddit(**kwargs)

    # Redditor
    @request_decorator.make_request
    def get_redditor(self, name):
        return Redditor(self._reddit, name=name)

    @request_decorator.make_request
    def get_redditor_submissions(self, redditor, *args, **kwargs):
        return redditor.submissions.top(*args, **kwargs)

    # Comment
    @request_decorator.make_request
    def get_comment_from_url(self, url):
        return Comment(self._reddit, url=url)

    @request_decorator.make_request
    def get_comment_from_id(self, id):
        return Comment(self._reddit, id=id)

    @request_decorator.make_request
    def get_parent_comment(self, comment):
        parent_comment = comment.parent()

        if isinstance(parent_comment, Comment):
            return parent_comment

    @request_decorator.make_request
    def get_child_comments(self, comment):
        comment.refresh()
        child_comment_forest = comment.replies
        child_comment_forest.replace_more()
        child_comments = child_comment_forest.list()

        return child_comments

    @classmethod
    def get_links_from_comment(self, comment):
        """
        Given the text of a reddit comment, finds all links with format [text](link)
        """
        body = comment.body
        matches = re.finditer(self._link_regex, body)

        links = []
        for match in matches:
            try:
                text = match.group(1).strip()
                link = match.group(2).strip()
                links.append((text, link))
            except:
                pass

        return links
