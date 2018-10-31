import os
import shutil
import subprocess


def run_cookie_daemon(kokoro_artifacts_dir):
    gcompute_tools = os.path.join(kokoro_artifacts_dir, "gcompute-tools")
    subprocess.check_call(
        [
            "git",
            "clone",
            "https://gerrit.googlesource.com/gcompute-tools",
            gcompute_tools,
        ]
    )
    subprocess.check_call([os.path.join(gcompute_tools, "git-cookie-authdaemon")])


def clone_git_on_borg_repo():
    cwd = os.getcwd()

    repo_name = "library-reference-docs"
    subprocess.check_call(
        [
            "git",
            "clone",
            "https://devrel.googlesource.com/cloud-docs/library-reference-docs",
        ]
    )
    os.chdir(repo_name)
    subprocess.check_call(
        [
            "git",
            "remote",
            "add",
            "direct",
            "https://devrel.googlesource.com/_direct/cloud-docs/library-reference-docs",
        ]
    )
    os.chdir(cwd)

    return repo_name


def push_changes(language, package, version):
    subprocess.check_call(["git", "add", "."])
    subprocess.check_call(["git", "status"])
    commit_msg = "Publish documentation for {}/{}/{}".format(language, package, version)
    subprocess.check_call(["git", "commit", "-m", commit_msg])
    subprocess.check_call(["git", "push", "direct", "master"])


def main():
    kokoro_artifacts_dir = os.environ["KOKORO_ARTIFACTS_DIR"]
    package = os.environ["PACKAGE"]
    language = os.environ["PACKAGE_LANGUAGE"]
    version = os.environ["PACKAGE_VERSION"]
    package_documentation = os.environ["PACKAGE_DOCUMENTATION"]

    run_cookie_daemon(kokoro_artifacts_dir)

    repo = clone_git_on_borg_repo()

    # Copy docs to repo
    dest = os.path.join(repo, language, package, version)
    if os.path.isdir(dest):
        shutil.rmtree(dest)

    shutil.copytree(
        package_documentation, os.path.join(repo, language, package, version)
    )
    os.chdir(repo)
    push_changes(language, package, version)  # Commit and push


if __name__ == "__main__":
    main()
