import enum
import os
import re
import csv
from time import sleep

import requests
from bs4 import BeautifulSoup
import config as conf
from config import GitHubPostType
from progress_bar import ProgressBar
import common


class Crawler:
    BASE_GITHUB_URL = "https://github.com/"
    TYPE_ISSUE = "Issues"
    TYPE_PULL_REQUEST = "Pull Requests"

    def __init__(self, repoName: str, options: list, keywords: list):
        print("="*(len(repoName)+4))
        print("  " + repoName)
        print("="*(len(repoName)+4))
        self._repoName = repoName
        self._options = options
        self._keywords = keywords
        self.issues = {}
        self.pullRequests = {}
        self._buildUrl()


    def checkIssues(self) -> list:
        return self._check(self.TYPE_ISSUE)
    

    def checkPullRequests(self) -> list:
        return self._check(self.TYPE_PULL_REQUEST)

        
    def saveResults(self, outDir: str) -> None:
        print("Save results to files .... ", end="")
        repoDir = os.path.join(outDir, self._repoName.replace('/', '_'))
        common.mkdir_if_not_exists(outDir)
        common.mkdir_if_not_exists(repoDir)
        res_vars = []
        if self.issues:
            res_vars.append(("issue_urls", "issues", self.issues))
        if self.pullRequests:
            res_vars.append(("pull_request_urls", "pull_requests", self.pullRequests))

        for urlFile, dirName, res in res_vars:
            f_urls = open(os.path.join(repoDir, urlFile), \
                'w', encoding='utf-8' ,newline="")
            for num in res:
                url = res[num][0]
                f_urls.write(url+"\n")
                contents = res[num][1]
                resDir = os.path.join(repoDir, dirName)            
                common.mkdir_if_not_exists(resDir)
                with open(os.path.join(resDir, str(num)), 
                    'w', encoding='utf-8' ,newline="") as f_res:
                    for c in contents:
                        f_res.write(str(c))
            f_urls.close()
        print("DONE\n")
        



    #########################
    #   Private Functions   #
    #########################
    def _buildUrl(self):
        '''
        Build a url string for the given repo name, options, and keywords.
        '''
        optStr = {
            GitHubPostType.ISSUE: "is%3Aissue",
            GitHubPostType.PULL_REQUEST: "is%3Apr",
            GitHubPostType.OPEN: "is%3Aopen",
            GitHubPostType.CLOSED: "is%3Aclosed",
        }

        url = os.path.join(self.BASE_GITHUB_URL, self._repoName)
        url = os.path.join(url, "issues?q=")
        url += '+'.join([ k.lower() for k in self._keywords])
        if GitHubPostType.ISSUE in self._options:
            self._issue_url = url + '+' + optStr[GitHubPostType.ISSUE]
        if GitHubPostType.PULL_REQUEST in self._options:
            self._pull_request_url = url + '+' + optStr[GitHubPostType.PULL_REQUEST]


    def _getTotalPages(self, issueListUrl: str) -> int:
        '''
        Get total number of pages from the webpage.
        '''
        t_pages = 0
        try:
            response = requests.get(issueListUrl)
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.find('em', attrs={"class":"current"})
            t_pages = int(str(text).split('data-total-pages="')[1].split('"')[0])
        except:
            t_pages = 1
        return t_pages

    def _getIssueNums(self, issuePageUrl: str) -> set:
        '''
        Get issue numbers on the current page.
        '''
        sleep(1)
        nums = set()
        try:
            response = requests.get(issuePageUrl)
            soup = BeautifulSoup(response.text, 'html.parser')
            issue_num_strs = re.findall(r"issue\_[0-9]+", str(soup.get_text))
            nums = [int(s.split('_')[1]) for s in issue_num_strs]
        except:
            exit(' - [!] Error while getting issue numbers.')
        return nums


    def _check(self, t: str) -> list:
        
        # Get URLs.
        print("Crawl " + t)
        url, pageName = (self._issue_url, "issues") \
            if t == self.TYPE_ISSUE else (self._pull_request_url, 'pull')

        t_pages = self._getTotalPages(url)
        issue_nums = []
        p_bar = ProgressBar(t_pages, ' - List', 30)
        p_bar.start()
        for p_num in range(1, t_pages+1):
            p_bar.update()
            p_url = url +'&page=' + str(p_num)
            nums = self._getIssueNums(p_url)
            issue_nums += nums

        # Find issue URLs in descending order.
        nums = sorted(list(set(nums)), reverse=True)
        nums += \
            [n for n in  range(1, nums[-1])[::-1]] if t_pages > 40 else []
        if len(nums) != 0:
            p_bar = ProgressBar(len(nums), ' - Page', 30)
            p_bar.start()
            for i, num in enumerate(nums):
                p_bar.update()
                url = os.path.join(self.BASE_GITHUB_URL, 
                    self._repoName, pageName, str(num))
                related, contents = c._isRelated(url) 
                if i < 1000 or related:
                    if t == self.TYPE_ISSUE:
                        self.issues[num] = (url, contents)
                    else:
                        self.pullRequests[num] = (url, contents)
                    


    def _isRelated(self, url: str) -> tuple:
        '''
        Check if the issue is related.
        '''
        sleep(1)
        related, contents = True, []
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            contents.append(str(soup.find('span', \
                attrs={"class":"js-issue-title"}) \
                ).lower())
            contents += soup.findAll('td', \
                attrs={"class":"comment-body"})
            
            # Check if it is related.
            for keyword in self._keywords:
                found = False
                for c in contents:
                    if keyword.lower() in c.lower():
                        found = True
                if not found: 
                    related = False
                    break
        except:
            related = False
        return related, contents

        




#####################
#   Main Function   #
#####################
if __name__ == "__main__":
    common.mkdir_if_not_exists(conf.OUT_DIR)

    # Read GitHub repo names.
    f_repos = open(conf.FILE_REPO_NAMES, encoding='utf-8',)
    reader = csv.reader(f_repos)
    repos = [repo[0] for repo in reader]
    f_repos.close()

    # Search 
    for repo in repos:
        c = Crawler(repo, conf.OPTIONS, conf.KEYWORDS)
        c.checkIssues()
        c.checkPullRequests()
        c.saveResults(conf.OUT_DIR)
        sleep(len(c.issues) + len(c.pullRequests))
        
        
