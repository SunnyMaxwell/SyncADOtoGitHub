import os
import shutil
import subprocess
import sys

def main(GitHubDestinationPAT, ADOSourcePAT, AzureRepoName, ADOCloneURL, GitHubCloneURL):
    print(' - - - - - - - - - - - - - - - - - - - - - - - - -')
    print(' reflect Azure Devops repo changes to GitHub repo')
    print(' - - - - - - - - - - - - - - - - - - - - - - - - - ')
    stage_dir = os.getcwd()
    print(f"stage Dir is: {stage_dir}")
    github_dir = os.path.join(stage_dir, "gitHub")
    print(f"github Dir: {github_dir}")
    destination = os.path.join(github_dir, AzureRepoName + ".git")
    print(f"destination: {destination}")
    # Please make sure, you remove https from azure-repo-clone-url
    source_url = f"https://{ADOSourcePAT}@{ADOCloneURL}"
    print(f"source URL: {source_url}")
    # Please make sure, you remove https from github-repo-clone-url
    dest_url = f"https://{GitHubDestinationPAT}@{GitHubCloneURL}"
    print(f"dest URL: {dest_url}")
    # Check if the parent directory exists and delete
    if os.path.exists(github_dir):
        shutil.rmtree(github_dir)
    if not os.path.exists(github_dir):
        os.makedirs(github_dir)
        os.chdir(github_dir)
        subprocess.run(["git", "clone", "--mirror", source_url])
    else:
        print(f"The given folder path {github_dir} already exists")
    os.chdir(destination)
    print('*****Git removing remote secondary****')
    subprocess.run(["git", "remote", "rm", "secondary"])
    print('*****Git remote add****')
    subprocess.run(["git", "remote", "add", "--mirror=fetch", "secondary", dest_url])
    print('*****Git fetch origin****')
    subprocess.run(["git", "fetch", source_url])
    print('*****Git push secondary****')
    subprocess.run(["git", "push", "secondary", "--all", "-f"])
    print('**Azure Devops repo synced with Github repo**')
    os.chdir(stage_dir)
    if os.path.exists(github_dir):
        shutil.rmtree(github_dir)
    print("Job completed")

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python script.py GitHubDestinationPAT ADOSourcePAT AzureRepoName ADOCloneURL GitHubCloneURL")
        sys.exit(1)
    GitHubDestinationPAT, ADOSourcePAT, AzureRepoName, ADOCloneURL, GitHubCloneURL = sys.argv[1:]
    main(GitHubDestinationPAT, ADOSourcePAT, AzureRepoName, ADOCloneURL, GitHubCloneURL)
