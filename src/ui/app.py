import sys
import random
from PySide2.QtWidgets import (
    QApplication,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QInputDialog,
    QTextBrowser,
)
from PySide2.QtCore import Qt, Slot, QRunnable, QThreadPool

from src.reddit import Reddit
from src.switcheroo.config import config
from src.switcheroo.main import get_links_from_comment


def find_next_switcheroo(reddit, link):
    comment = reddit.get_comment_from_url(link)
    found_links = get_links_from_comment(reddit, comment)

    if not found_links:
        print(f"Oh no! No links were found in comment {comment.id}. Halting crawl.")
        return None

    link = found_links[0]
    return link[1]


class Worker(QRunnable):
    def __init__(self, text, first_link):
        super(Worker, self).__init__()
        self.text = text
        self.first_link = first_link
        self._add_link(self.first_link)

    def _add_link(self, link):
        self.text.append(f'<a href="{link}" title="{link}">{link}</a>')

    def run(self):
        reddit = Reddit(
            client_id=config.client_id,
            client_secret=config.client_secret,
            user_agent=config.user_agent,
        )

        active_link = self.first_link
        while True:
            active_link = find_next_switcheroo(reddit, active_link)
            if not active_link:
                break

            self._add_link(active_link)

        self.text.append("All done!")


class App(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.threadpool = QThreadPool()

        self.text = QTextBrowser()
        # self.text.setReadOnly(True)
        self.text.setOpenLinks(True)
        self.text.setOpenExternalLinks(True)
        self.text.setAlignment(Qt.AlignBottom)

        self.input = QInputDialog()
        self.input.setLabelText("Enter a switcheroo link")

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.text)
        self.setLayout(self.layout)

        self.input.textValueSelected.connect(self.follow_link)

    @Slot()
    def follow_link(self):
        first_link = self.input.textValue()

        worker = Worker(self.text, first_link)
        self.threadpool.start(worker)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = App()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec_())
