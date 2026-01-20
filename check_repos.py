import requests

print("Checking public repositories for user: racingdna46-code")
url = "https://api.github.com/users/racingdna46-code/repos"
try:
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        repos = response.json()
        print(f"Found {len(repos)} public repositories:")
        found = False
        for repo in repos:
            print(f"- {repo['name']} ({repo['html_url']})")
            if repo['name'].lower() == 'sattva_sound_engine':
                found = True
        
        if found:
            print("\nSUCCESS: 'sattva_sound_engine' is visible in the public list.")
        else:
            print("\nFAILURE: 'sattva_sound_engine' is NOT in the public list.")
    else:
        print(f"Error: {response.text}")

except Exception as e:
    print(f"Exception: {e}")
