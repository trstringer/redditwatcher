from datetime import datetime
import sys
import os
import praw
import colorama


def main():
    colorama.init()

    reddit = praw.Reddit(
        client_id=os.environ['REDDITWATCHER_CLIENTID'],
        client_secret=os.environ['REDDITWATCHER_CLIENTSECRET'],
        user_agent='redditwatcher'
    )

    try:
        for submission in (
                reddit.subreddit(subreddits(sys.argv)).stream.submissions()):
            display_submission(submission)
    except KeyboardInterrupt:
        pass


def subreddits(args):
    return '+'.join(args[1:])


def display_submission(submission):
    print('{}/r/{} {}[{}] {}{} {}{}'.format(
        colorama.Fore.GREEN,
        submission.subreddit.display_name,
        colorama.Fore.BLUE,
        '{d.month}/{d.day} {d.hour}:{d.minute:02} {d:%P}'.format(
            d=datetime.fromtimestamp(submission.created_utc)
        ),
        colorama.Fore.YELLOW,
        submission.shortlink,
        colorama.Fore.RESET,
        submission.title
    ))


if __name__ == '__main__':
    main()
