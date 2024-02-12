# this is a basic script that will pull SMTP credentials for a mailgun account in both US and EU regions

import requests
import logging
from getpass import getpass

logging.basicConfig(filename='requests.log', level=logging.INFO, filemode='a')

def check_domains_in_region(session, region):
    resp = get_domains(session, region)
    if resp.status_code == 200:
        account_domains = resp.json()['items']
        for domain in account_domains:
            return True
    return False

def get_api_key():
    api_key = None
    if api_key is None:
        api_key = getpass("Please enter your API Key: ")
    return api_key

def get_base_url(region):
    if region == 'eu':
        return "https://api.eu.mailgun.net"
    else:
        return "https://api.mailgun.net"

def get_credentials(session, domain, region):
    base_url = get_base_url(region)
    return session.get(
        f"{base_url}/v3/domains/{domain}/credentials",
        auth=("api", api_key))

def get_domains(session, region):
    base_url = get_base_url(region)
    return session.get(
        f"{base_url}/v3/domains",
        auth=("api", api_key),
        params={"limit": 100})

def main():
    global api_key
    api_key = get_api_key()

    with requests.Session() as session:
        if check_domains_in_region(session, 'us'):
            process_domains(session, 'us')
        if check_domains_in_region(session, 'eu'):
            process_domains(session, 'eu')

def process_domains(session, region):
    resp = get_domains(session, region)
    if resp.status_code == 200:
        logging.info(f"Request to get domains in {region} region successful!")
        account_domains = resp.json()['items']
        for domain in account_domains:
            domain_name = domain['name']
            credentials_raw = get_credentials(session, domain_name, region)
            if credentials_raw.status_code == 200:
                credentials = credentials_raw.json()['items']
                logging.info(f"Request to get SMTP creds for domain {domain_name} in {region} region successful!")
                print(f"Credentials for domain {domain_name} in {region} region")
                for credential in credentials:
                    login = credential.get('login', '')
                    created_at = credential.get('created_at', '')
                    print(f"Login: {login}")
                print("\n")
            else:
                logging.error(f"Failed to fetch credentials for domain {domain_name} in {region} region: {credentials_raw.status_code}")
    else:
        print(f"Failed to get domains in {region} region: {resp.status_code}")
        logging.error(f"Failed to get domains in {region} region: {resp.status_code}")

if __name__ == "__main__":
    main()
