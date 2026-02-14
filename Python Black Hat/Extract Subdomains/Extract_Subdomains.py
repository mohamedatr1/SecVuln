import requests
import string
from concurrent.futures import ThreadPoolExecutor

url = "google.com"
max_letters = 3  
threads = 10

def check_subdomain(subdomain):
    full_domain = f"{subdomain}.{url}"
    try:
        
        response = requests.get(f"http://{full_domain}", timeout=3)
        if response.status_code in [200, 301, 302]:
            print(f"[+] Founded: {full_domain} | {response.status_code}")
            return full_domain
    except requests.exceptions.RequestException:
        pass
    return None

def generate_subdomains(letters, length):
    
    if length == 1:
        return list(letters)
    else:
        return [f"{letter}{sub}" for letter in letters for sub in generate_subdomains(letters, length - 1)]

def start_bruteforce():
    letters = string.ascii_lowercase
    print(f"[*] Starting Bruteforce on {url} with {threads} threads...")
    
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for length in range(1, max_letters + 1):
            subdomains_list = generate_subdomains(letters, length)
            
            executor.map(check_subdomain, subdomains_list)

if __name__ == "__main__":
    start_bruteforce()