# 9_github_trending

The program looks for newly created repositories that have the most stars and then shows the amount of open issues. You can specify how many top repositories you want to see and how new they should be.

The result looks this way (for each repository in the top list):   
> Repository "arithmetic" of user "vasya" has 42 opened issues. Link: https:<i></i>//github.com/v<i></i>vasya/arithmetic

### Parameters:   
**--count** - the amount of repositories to show, default = 5   
**--time** - maximum age of repositories (in days), default = 7   
**--exclude_pull_requests** - counts only issues, ignores pull requests   

### Usage examples:

> python github_trending.py --count 8 --time 14   

This shows eight most 'starred' repositories created in the last fortnight.   

> python github_trending.py --count 2 --exclude_pull_requests   

This shows two most trending repositories not older than a week, and only issues are displayed.

### P.S.

Be aware that as this program doesn't use any form of authentication, you will be limited to 60 API requests per hour.
