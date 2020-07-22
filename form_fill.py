from urllib.parse import urljoin
import webbrowser
from get_Forms_and_inputs import *


first_form = get_all_forms(url)[0]
form_details = get_form_details(first_form)

data = {}
for input_tag in form_details["inputs"]:
    if input_tag["type"] == "hidden":
        # if it's hidden, use the default value
        data[input_tag["name"]] = input_tag["value"]
    elif input_tag["type"] != "submit":
        # all others except submit, prompt the user to set it
        value = input(f"Enter the value of the field '{input_tag['name']}' (type: {input_tag['type']}): ")
        data[input_tag["name"]] = value

# join the url with the action (form request URL)
url = urljoin(url, form_details["action"])
print(url)
print("*"*50)
if form_details["method"] == "post":
    res = session.post(url, data=data)
    print(res)
elif form_details["method"] == "get":
    res = session.get(url, params=data)

print("=="*50)
print(res)