import subprocess
import requests
import json
import os

# Configuration
LOCAL_DIR = "D:/tutorial/nodereactedashbd"
GITHUB_USER = "aespitoj"
REPO_NAME = "Edashboard4"
GITHUB_TOKEN = os.getenv("GH_TOKEN")  # Ensure GH_TOKEN is set as an environment variable

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

def create_github_repo():
    """Creates a new repository on GitHub if it doesn't exist."""
    url = f"https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "name": REPO_NAME,
        "private": False
    }
    
    # Check if repository exists
    repo_url = f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}"
    response = requests.get(repo_url, headers=headers)
    
    if response.status_code == 404:
        # Repository does not exist, create it
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 201:
            print(f"Repository '{REPO_NAME}' created successfully.")
        else:
            print(f"Failed to create repository: {response.json()}")
    else:
        print(f"Repository '{REPO_NAME}' already exists.")
    
def init_git_repo():
    """Initializes a Git repository and sets up the remote origin."""
    print("Initializing git repository...")
    run_command(["git", "init"], cwd=LOCAL_DIR)

    # Check if the remote already exists
    print("Checking existing remotes...")
    try:
        result = subprocess.run(["git", "remote", "-v"], cwd=LOCAL_DIR, text=True, capture_output=True, check=True)
        if "origin" in result.stdout:
            print("Remote origin already exists. Updating remote URL...")
            run_command(["git", "remote", "set-url", "origin", f"https://{GITHUB_USER}:{GITHUB_TOKEN}@github.com/{GITHUB_USER}/{REPO_NAME}.git"], cwd=LOCAL_DIR)
        else:
            print("Adding remote origin...")
            run_command(["git", "remote", "add", "origin", f"https://{GITHUB_USER}:{GITHUB_TOKEN}@github.com/{GITHUB_USER}/{REPO_NAME}.git"], cwd=LOCAL_DIR)
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
    try:
        run_command(["git", "push", "-u", "origin", "main"], cwd=LOCAL_DIR)
    except subprocess.CalledProcessError as e:
        if "This repository moved" in e.stderr:
            print("Repository has moved. Updating remote URL...")
            # Update the remote URL to the new location
            new_remote_url = "https://github.com/aespitoj/Edashboard-manual.git"
            run_command(["git", "remote", "set-url", "origin", new_remote_url], cwd=LOCAL_DIR)
            # Retry the push
            print("Retrying push to GitHub...")
            run_command(["git", "push", "-u", "origin", "main"], cwd=LOCAL_DIR)

if __name__ == "__main__":
    create_github_repo()
    init_git_repo()
    add_and_commit_changes()
    push_to_github()
