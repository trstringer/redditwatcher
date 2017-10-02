from datetime import datetime
import sys
import os
import praw
from version import VERSION


def main():

    if len(sys.argv) < 2:
        print('You must specify a subreddit or multiple subreddits (or --version)')
        sys.exit(1)

    if sys.argv[1] in ['--version', '-v']:
        print('redditwatcher v{}'.format(VERSION))
        sys.exit(0)

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
    created = datetime.fromtimestamp(submission.created_utc)
    adjusted_hour = created.hour if created.hour <= 12 else created.hour - 12
    if adjusted_hour == 0:
        adjusted_hour = 12
    adjusted_minute = str(created.minute).rjust(2, '0')

    print('/r/{} [{}] {}\n   ======> {}\n'.format(
        submission.subreddit.display_name,
        '{}/{} {}:{} {}'.format(
            created.month, created.day,
            adjusted_hour, adjusted_minute,
            created.strftime('%P')
        ),
        submission.shortlink,
        submission.title
    ))


if __name__ == '__main__':
    main()
