from doctest import OutputChecker
import enum

########################
#   GitHub Post Type   #
########################
class GitHubPostType(enum.Enum):
   ISSUE = "is%3Aissue"
   PULL_REQUEST = "is%3Apr"
   OPEN = "is%3Aopen"
   CLOSED = "is%3Aclosed"
   


################
#   Settings   #
################
ENABLE_PROGRESS_BAR = True
OUT_DIR = "out"
FILE_REPO_NAMES = "github_repos.csv"

OPTIONS = [
    GitHubPostType.ISSUE,
    GitHubPostType.PULL_REQUEST
]

KEYWORDS = [
    "crash", 
    "android", 
    "version", 
    "device",
]


   
