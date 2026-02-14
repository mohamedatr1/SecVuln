import requests

url = "http://testphp.vulnweb.com/"
input_file = r"C:\Users\IT DOCTOR\Downloads\My Python\Python Black Hat\Extract Hidden Paths\path.txt" 

def search_paths(url,input_file):
    with open(input_file, 'r') as f:
        paths = f.readlines()
    for path in paths:
        path = path.strip()
        new_url = f"{url}/{path}"
        response = requests.get(new_url)
        if response.status_code == 200:
            print(f"[+] Found: {new_url} - Status : 200")
        elif response.status_code == 404:
            print(f"[-] Found: {new_url} - Status : 404")
        else:
            print(f"[-] Not Found: {response.status_code}")

search_paths(url,input_file)