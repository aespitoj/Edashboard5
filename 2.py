import subprocess
import os

# Configuration
LOCAL_DIR = "D:/tutorial/nodereactedashbd"
GITHUB_USER = "aespitoj"
REPO_NAME = "Edashboard2"

def run_command(command, cwd=None):
    """Executes a command and prints the output."""
    try:
        result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=True)
        print(f"Command: {' '.join(command)}")
        print(f"Output: {result.stdout}")
        print(f"Error: {result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Command: {' '.join(command)}")
        print(f"Output: {e.output}")
        print(f"Error: {e.stderr}")

def init_git_repo():
    """Initializes a Git repository and sets up the remote origin."""
    print("Initializing git repository...")
    run_command(["git", "init"], cwd=LOCAL_DIR)

    # Check if the remote already exists
    print("Checking existing remotes...")
    try:
        result = subprocess.run(["git", "remote", "-v"], cwd=LOCAL_DIR, text=True, capture_output=True, check=True)
        if "origin" in result.stdout:
            print("Remote origin already exists.")
        else:
            print("Adding remote origin...")
            run_command(["git", "remote", "add", "origin", f"https://github.com/{GITHUB_USER}/{REPO_NAME}.git"], cwd=LOCAL_DIR)
    except subprocess.CalledProcessError as e:
        print(f"Error checking remote: {e}")

def add_and_commit_changes():
    """Adds and commits all changes to the local repository."""
    print("Adding changes...")
    run_command(["git", "add", "--all"], cwd=LOCAL_DIR)  # Use --all to add all changes including untracked files
    print("Committing changes...")
    run_command(["git", "commit", "-m", "Initial commit"], cwd=LOCAL_DIR)

def push_to_github():
    """Pushes changes to GitHub."""
    print("Pushing to GitHub...")
    run_command(["git", "push", "-u", "origin", "main"], cwd=LOCAL_DIR)

if __name__ == "__main__":
    init_git_repo()
    add_and_commit_changes()
    push_to_github()
