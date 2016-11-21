import argparse
import datetime
import requests


def get_trending_repositories(top_size, days_count):
    """
    Finds %top_size% repositories with the largest amount of stars
    created in the last %days_number% days.
    :returns (username, repo_name, repo_link) generator
    """
    delay = datetime.timedelta(days=days_count)
    earliest_date = datetime.date.today() - delay
    queue = 'created:>{}'.format(earliest_date)
    payload = {'q': queue, 'sort': 'stars', 'order': 'desc'}
    base = 'https://api.github.com/search/repositories'
    response = requests.get(base, params=payload)
    if response.status_code != requests.codes.ok:
        return None
    response_json = response.json()
    for repository in response_json['items'][:top_size]:
        yield repository['owner']['login'],\
            repository['name'],\
            repository['html_url'],\
            repository['open_issues_count']


def get_open_issues_amount(repo_owner, repo_name):
    """
    Counts the amount of open issues for a repository, excluding open pull requests.
    Each call of this functions requires a request to GitHub.
    """
    payload = {'state': 'open'}
    base = 'https://api.github.com/repos/{}/{}/issues'.format(repo_owner, repo_name)
    response = requests.get(base, params=payload)
    if response.status_code != requests.codes.ok:
        return None
    issues = list(filter(lambda issue: 'pull_request' not in issue, response.json()))
    return len(issues)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--count', action='store', type=int, dest='count', default=5,
                        help='the amount of repositories you want to retrieve')
    parser.add_argument('--time', action='store', type=int, dest='time_period', default=7,
                        help='repositories should not be older than this (in days)')
    parser.add_argument('--exclude_pull_requests', action='store_true', dest='exclude_pull_requests')
    parser.set_defaults(exclude_pull_requests=False)
    return parser.parse_args()


def reply_include_pull_requests(repository):
    """
    Tells the amount of open issues, including pull requests.
    Requires as much API requests to GitHub as there are repositories you want to display.
    """
    repo_owner, repo_name, repo_link, repo_open_issues = repository
    reply_string = 'Repository "{}" of user "{}" has {} open issues and pull requests. Link: {}'\
        .format(repo_name,
                repo_owner,
                repo_open_issues,
                repo_link)
    return reply_string


def reply_exclude_pull_requests(repository):
    """
    Tells the amount of open issues, excluding pull requests.
    Requires only one API request to GitHub.
    Default option.
    """
    repo_owner, repo_name, repo_link, repo_open_issues = repository
    reply_string = 'Repository "{}" of user "{}" has {} open issues. Link: {}'\
        .format(repo_name,
                repo_owner,
                get_open_issues_amount(repo_owner, repo_name),
                repo_link)
    return reply_string


if __name__ == '__main__':
    arguments = parse_arguments()
    repositories = get_trending_repositories(arguments.count, arguments.time_period)
    if repositories is None:
        print('HTTP request failed, something went wrong. Try to try again later.')
        raise SystemExit
    if arguments.exclude_pull_requests:
        get_reply_string = reply_exclude_pull_requests
    else:
        get_reply_string = reply_include_pull_requests
    for repository in repositories:
        reply_string = get_reply_string(repository)
        print(reply_string)
