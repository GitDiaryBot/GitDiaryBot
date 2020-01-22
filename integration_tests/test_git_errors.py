import os
import shutil

import git

from diarybot.git_sync import GitSync


HERE = os.path.dirname(__file__)
UPSTREAM_DIR = os.path.join(HERE, 'upstream')
GIT_DIR = os.path.join(HERE, 'git_dir')
FILE_PATH = os.path.join(GIT_DIR, 'file')
DIRTY_FILE = os.path.join(GIT_DIR, 'dirty')


def create_bare_repo(git_dir) -> git.Repo:
    if os.path.exists(git_dir):
        shutil.rmtree(git_dir)
    os.makedirs(git_dir)
    return git.Repo.init(git_dir, bare=True)


def add_empty_file(repo, file_name):
    open(file_name, 'wb').close()
    repo.index.add([file_name])


def commit_empty_file(repo, file_name):
    add_empty_file(repo, file_name)
    repo.index.commit("commit")


def clone(git_dir, orig_repo):
    if os.path.exists(git_dir):
        shutil.rmtree(git_dir)
    return orig_repo.clone(git_dir)


def test_dirty_tree_on_pull():
    upstream = create_bare_repo(UPSTREAM_DIR)
    repo = clone(GIT_DIR, upstream)
    git_sync = GitSync(GIT_DIR)
    open(FILE_PATH, 'wb').close()
    git_sync.on_after_write()
    add_empty_file(repo, DIRTY_FILE)
    git_sync.on_before_write()
    git_sync.on_after_write()
