# GitHub Issue Crawler
This tool is designed to crawl issues from multiple GitHub repositories with the provided keywords. 
It gives numbers of all the related issues and scrapes contents of each issue. 

## How to Use
In **_config.py_** file, a user can configure settings such as keywords to search, a file path for the repo names, and output director.

1. Install required packages.
```sh
    $ python3 -m pip install bs4 requests 
```

2. Run the main python program. 
```sh
    $ python3 crawler.py 
```

3. Results
By default, the results are stored under **_out/_** directgory, and here are details of the results:

    out/
    ├── ...
    ├── repo_name/
    │   ├── issue_urls
    │   ├── pull_requests_urls
    │   ├── issues/
    │   │   ├── 1001
    │   │   ├── ...
    │   │   └── 203 
    │   └── pull_requests\
    │       ├── 1002
    │       ├── ...
    │       └── 135 
    └── ...

