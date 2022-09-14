from operator import index
import requests
import csv

api_key = input("Please enter API key")
domains_array = []
domains_need_certs = []

def get_domains():
    return requests.get(
        "https://api.mailgun.net/v3/domains",
        auth=("api", f"{api_key}"),
        params={"skip": 0,
                "limit": 999}).json() 
def cert_gen(domain_name):
        return requests.post(
        f"https://api.mailgun.net/v1/x509/email.{domain_name}",
        auth=("api", f"{api_key}"))

r = get_domains()
items = r['items']

for objects in items:
    domain_name= objects['name']
    web_scheme = objects["web_scheme"]
    
    if web_scheme == "http":
        domains_array.append(objects)

file = open("domains_with_cname.csv", "w")
writer = csv.writer(file)

for w in range(len(domains_array)):
    writer.writerow([domains_array[w]])

file.close()