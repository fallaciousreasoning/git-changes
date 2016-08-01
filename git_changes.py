import re
import sys
import os
import subprocess

import tempfile

git_changes_by_author = 'git -C {} log --author="{}" --pretty=tformat: --numstat'
git_changes_regex = r'(\d+)\s+(\d+)\s+(.*)'

git_author_commits = 'git -C {} shortlog -s -n'
git_author_regex = r'(\d+)\s+(.*)'

git_repo = None

def get_authors():
    pattern = re.compile(git_author_regex)

    output = run_command(git_author_commits.format(git_repo))
    authors = []
    for line in output:
        matches = pattern.findall(line)
        for match in matches:
            authors.append(match[1])

    return authors


def counts_for_author(author):
    pattern = re.compile(git_changes_regex)

    output = run_command(git_changes_by_author.format(git_repo, author))

    additions = 0
    deletions = 0

    for line in output:
        matches = pattern.findall(line)

        if len(matches) == 0: continue

        match = matches[0]
        
        added = int(match[0])
        deleted = int(match[1])

        additions += added
        deletions += deleted

    return (additions, deletions)


def get_changes():
    authors = get_authors()

    changes = []
    for author in authors:
        counts = counts_for_author(author)
        changes.append((author, counts[0], counts[1]))

    return changes

def run_command(command):     
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    name = temp_file.name
    temp_file.close()

    os.system(command + ">" + name)

    with open(name, 'r') as f:
        return f.readlines()

git_repo = "seng440-project1"
if len(sys.argv) > 1:
    git_repo = sys.argv[1]

for change in get_changes():
    print(change[0])
    print('\tAdded:', change[1])    
    print('\tDeleted:', change[2])