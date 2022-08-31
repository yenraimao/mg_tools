from operator import index
import requests

#update the below to reflect API key
api_key = ""

# update the below to reflect domain that template is under
my_domain = 'jeremypockey.com'

# update the below to reflect your template name
template_name = 'mytemplate'

def get_template_version():
    return requests.get(
        f"https://api.mailgun.net/v3/{my_domain}/templates/{template_name}/versions/initial",
        auth=("api", f"{api_key}")).json()

r = get_template_version()
version = r['template']['version']

print(version)