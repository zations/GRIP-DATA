from git import Repo

repo = Repo(r"C:\Users\pavit\programing\GRIP\GRIP")

for commit in repo.iter_commits():
    files = list(commit.stats.files.keys())
    folder_groups = {f.split('/')[0] for f in files}
    print(commit.hexsha, commit.message, folder_groups)
