import requests
import os
import re

def check_domain(domain):
    try:
        response = requests.get(domain, timeout=10, allow_redirects=True)
        return response.status_code == 200
    except:
        return False

def get_current_domain():
    if os.path.exists("domain.txt"):
        with open("domain.txt", "r") as f:
            content = f.read().strip()
            match = re.search(r'guncel_domain=(https?://[^\s]+)', content)
            if match:
                return match.group(1)
    
    return "https://trgoals1397.xyz/"

def extract_domain_number(domain):
    match = re.search(r'trgoals(\d+)', domain)
    if match:
        return int(match.group(1))
    return 1397

def main():
    current_domain = get_current_domain()
    domain_number = extract_domain_number(current_domain)
    
    print(f"Mevcut domain: {current_domain}")
    print(f"Domain numarası: {domain_number}")
    
    # Mevcut domaini kontrol et
    current_active = check_domain(current_domain)
    print(f"Mevcut domain aktif mi: {current_active}")
    
    # Bir üst domaini kontrol et
    next_domain = f"https://trgoals{domain_number + 1}.xyz/"
    next_active = check_domain(next_domain)
    print(f"Bir üst domain aktif mi: {next_active}")
    
    # Hangi domainin kullanılacağını belirle
    if next_active:
        selected_domain = next_domain
        should_update = True
        print(f"Bir üst domain aktif, kullanılacak: {selected_domain}")
    else:
        selected_domain = current_domain
        should_update = False
        print(f"Bir üst domain aktif değil, mevcut domain korunacak: {selected_domain}")
    
    # domain.txt dosyasını güncelle (gerekirse)
    if should_update:
        with open("domain.txt", "w") as f:
            f.write(f"guncel_domain={selected_domain}")
        print(f"::set-output name=updated::true")
        print(f"::set-output name=selected_domain::{selected_domain}")
    else:
        print(f"::set-output name=updated::false")

if __name__ == "__main__":
    main()
