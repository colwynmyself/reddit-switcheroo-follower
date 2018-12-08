# Reddit Switcheroo Follower

This is a silly weekend project to follow one of the "Old Reddit Switcheroo" links until the end.

## Setup

* Get `pyenv` and `pyenv-virtualenv`
* `pip install pipenv`
* `pipenv install --dev`

## Following A Link

Go to reddit and grab the permalink for the link you want to follow.

Run `python -m src.main -c <url>`
