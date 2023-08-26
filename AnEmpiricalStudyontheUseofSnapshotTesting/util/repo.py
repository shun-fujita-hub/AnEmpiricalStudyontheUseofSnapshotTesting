import os

import pygit2
from pygit2 import GIT_RESET_HARD

from AnEmpiricalStudyontheUseofSnapshotTesting.settings import clone_repo_base_dir


def clone(name):
    cloned_repo_dir = f"{clone_repo_base_dir}/{name}"
    # cloned_repo_dir = f"/work/kashiwa/repos/{name}"
    try:
        pygit2.clone_repository(f"https://github.com/{name}", cloned_repo_dir)
        raise
        # print(f"mkdir -p {cloned_repo_dir}")
        # print(f"git clone https://github.com/{name} {cloned_repo_dir}")
    except ValueError:
        print("repository has already existed")
        pass
    return cloned_repo_dir


def checkout(cloned_repo_dir, sha):
    repo = pygit2.Repository(cloned_repo_dir)
    repo.reset(sha, GIT_RESET_HARD)


if __name__ == "__main__":
    repo_dir = clone("juliomrqz/statusfy")
    checkout(repo_dir, "823ce735f90fbefd0bfa71926d2adf551ea2b43e")




