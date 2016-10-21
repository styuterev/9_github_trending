# 9_github_trending

The program looks for newly created repositories that have the most stars and then shows the amount of open issues and pull requests. You can specify how many top repositories you want to see and how new they should be.   

The result looks this way (for each repository in the top list):   
> Repository "arithmetics" of user "vasya" has 42 opened issues and pull requests. Link: https:<i></i>//github.com/v<i></i>asya/arithmetics

### Parameters:   
**--count** - the amount of repositories to show, default = 5   
**--time** - maximum age of repositories (in days), default = 7   

### Usage examples:

> python github_trending.py --count 8 --time 14   

This shows eight most 'starred' repositories created in the last fortnight.   

> python github_trending.py --count 2   

This shows wto most trending repos not older than a week.   

### P.S.

Be aware that as this program doesn't use any form of authentication, you will be limited to 60 API requests per hour.
