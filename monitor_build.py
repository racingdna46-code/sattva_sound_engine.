import requests
import time
import os
import zipfile
import shutil

REPO_OWNER = "racingdna46-code"
REPO_NAME = "sattva_sound_engine."
WORKFLOW_NAME = "Mac Build"
ARTIFACT_NAME = "macOS-App"
DIST_DIR = os.path.join(os.getcwd(), "dist")

def get_latest_workflow_run():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/runs"
    try:
        response = requests.get(url)
        response.raise_for_status()
        runs = response.json().get("workflow_runs", [])
        for run in runs:
            if run["name"] == WORKFLOW_NAME:
                return run
    except Exception as e:
        print(f"Error fetching runs: {e}")
    return None

def monitor_run(run_id):
    print(f"Monitoring Run ID: {run_id}")
    while True:
        url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/runs/{run_id}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            status = data["status"]
            conclusion = data["conclusion"]
            print(f"Status: {status}, Conclusion: {conclusion}")
            
            if status == "completed":
                return conclusion == "success"
        else:
            print(f"Failed to get run status: {response.status_code}")
        
        time.sleep(15)

def download_artifact(run_id):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/runs/{run_id}/artifacts"
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to list artifacts")
        return False
    
    artifacts = response.json().get("artifacts", [])
    download_url = None
    for artifact in artifacts:
        if artifact["name"] == ARTIFACT_NAME:
            download_url = artifact["archive_download_url"]
            print(f"Found artifact URL: {download_url}")
            break
            
    if not download_url:
        print("Artifact not found.")
        return False

    print("Downloading artifact... (Note: Public artifacts might require a token or browser session if API doesn't allow direct public access)")
    # For public repos, the archive_download_url redirects. Python requests handles redirects.
    # However, sometimes it requires auth. Let's try.
    try:
        r = requests.get(download_url, stream=True)
        # Check login page redirect
        if "login" in r.url:
            print("Error: GitHub requires login to download artifacts even from public repos via API.")
            print("Please download manually from: " + download_url)
            return False
            
        zip_path = os.path.join(DIST_DIR, "mac_app.zip")
        with open(zip_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        print("Download complete.")
        
        # Extract
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(DIST_DIR)
        print(f"Extracted to {DIST_DIR}")
        os.remove(zip_path)
        return True
    except Exception as e:
        print(f"Download failed: {e}")
        return False

def main():
    if not os.path.exists(DIST_DIR):
        os.makedirs(DIST_DIR)
        
    print("Waiting for workflow run to start...")
    # Poll for a recent run (created in last 5 mins)
    start_time = time.time()
    target_run = None
    
    while time.time() - start_time < 300: # Wait 5 mins for push/start
        run = get_latest_workflow_run()
        if run and run["status"] in ["queued", "in_progress"]:
            target_run = run
            break
        elif run and run["status"] == "completed":
             # check if it finished recently? Maybe user pushed earlier.
             # For now, let's assume we want a strictly new or running one.
             pass
        time.sleep(5)
        print(".", end="", flush=True)

    if not target_run:
        print("\nNo active workflow run found. Did the push succeed?")
        return

    success = monitor_run(target_run["id"])
    if success:
        print("Build successful. Attempting download...")
        download_artifact(target_run["id"])
    else:
        print("Build failed.")

if __name__ == "__main__":
    main()
