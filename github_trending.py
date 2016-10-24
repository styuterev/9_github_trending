import argparse
import datetime
import requests


def get_trending_repositories(top_size=5, days_count=7):
    """
    Finds %top_size% repositories with the largest amount of stars
    created in the last %days_number% days.
    """
    delay = datetime.timedelta(days=days_count)
    earliest_date = datetime.date.today() - delay
    queue = 'created:>{}'.format(earliest_date)
    payload = {'q': queue, 'sort': 'stars', 'order': 'desc'}
    base = 'https://api.github.com/search/repositories'
    response = requests.get(base, params=payload)
    success_code = 200
    if response.status_code != success_code:
        return None
    response_json = response.json()
    for repository in response_json['items'][:top_size]:
        yield (repository['owner']['login'], repository['name'], repository['html_url'])


def get_open_issues_amount(repo_owner, repo_name):
    """
    Finds repository called %repo_name% of user %repo_owner%.
    Counts open issues and open pull requests.
    """
    payload = {'state': 'open'}
    base = 'https://api.github.com/repos/{}/{}/issues'.format(repo_owner, repo_name)
    response = requests.get(base, params=payload)
    success_code = 200
    if response.status_code != success_code:
        return None
    response_json = response.json()
    return len(response_json)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--count', action='store', dest='count', default=5,
                        help='the amount of repositories you want to retrieve')
    parser.add_argument('--time', action='store', dest='time_period', default=7,
                        help='repositories should not be older than this (in days)')
    return parser.parse_args()


if __name__ == '__main__':
    arguments = parse_arguments()
    repositories = get_trending_repositories(int(arguments.count),
                                             int(arguments.time_period))
    if repositories is None:
        print('HTTP request failed, something went wrong. Try to try again later.')
        raise SystemExit
    for repository in repositories:
        repo_owner, repo_name, repo_link = repository
        reply_string = 'Repository "{}" of user "{}" has {} open' \
                       'issues and pull requests. Link: {}'.\
            format(repo_name, repo_owner, get_open_issues_amount(repo_owner, repo_name), repo_link)
        print(reply_string)
