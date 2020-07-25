from bs4 import BeautifulSoup
from requests_html import HTMLSession
import requests
from lxml import html
from urllib.parse import urljoin
import pandas as pd


# def get_captcha(soup):
#     captcha_src = soup.find_all("img")
#     for i in captcha_src:
#         if "Captcha" in i['src']:
#             return str(i['src'])


data = {
        'form_rcdl:tf_dlNO': "DL-0420110149646",
        'form_rcdl:tf_dob_input': "09-02-1976",
        'form_rcdl:j_idt32:CaptchaID': ""
    }

def start(data):
    session = HTMLSession()
    url = "https://parivahan.gov.in/rcdlstatus/?pur_cd=101"
    res = session.get(url)

    # ----------------FORM EXTRACTION----------------

    soup = BeautifulSoup(res.html.html, "html.parser")
    details = {}

    form = soup.find_all("form")[0]
    action = form.attrs.get("action").lower()
    method = form.attrs.get("method", "get").lower()
    inputs = []

    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        input_value = input_tag.attrs.get("value", "")
        inputs.append({"type": input_type, "name": input_name, "value": input_value})

    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs

    # -------------------Captcha---------------------
    captcha_src = soup.find_all("img")
    for i in captcha_src:
        if "Captcha" in i['src']:
            captcha_url = "https://parivahan.gov.in/" + i['src']

    print(captcha_url)  # Currently Captcha is taking by user input by visiting the link
    # -------------------FORM FILLING-----------------

    data['form_rcdl:j_idt32:CaptchaID'] = input("Enter Captcha: ")

    submit_url = urljoin(url, details["action"])
    #print(submit_url)

    if details["method"] == "post":
        res = session.post(submit_url, data=data)
        # return res
    elif details["method"] == "get":
        res = session.get(submit_url, params=data)
        # return res

    # ----------Authorization-----------

    auth_cookie = res.cookies

    # ---------Data Extract-------------

    name_xpath = '//*[@id="form_rcdl:j_idt115"]/table[1]/tbody/tr[2]/td[2]'
    issue_xpath = '//*[@id="form_rcdl:j_idt115"]/table[2]/tbody/tr[1]/td[2]/text()'
    expiry_xpath = '//*[@id="form_rcdl:j_idt115"]/table[2]/tbody/tr[1]/td[3]/text()'
    vehicle_class_xpath = '//*[@id="form_rcdl:j_idt164_data"]/tr/td[2]'
    driving_num_xpath = '//*[@id="form_rcdl:j_idt115"]/table[1]/tbody/tr[5]/td[2]'

    url = 'https://parivahan.gov.in/rcdlstatus/vahan/rcDlHome.xhtml'
    response = requests.get(url, cookies=auth_cookie)
    byte_data = response.content
    source_code = html.fromstring(byte_data)

    # --------------CSV DUMP----------------------
    final_data = [["Name"], ["Issue Date"], ["Expiry Date"], ["Vehicle Class"],]

    name_list = source_code.xpath(name_xpath)
    issue_list = source_code.xpath(issue_xpath)
    expiry_list = source_code.xpath(expiry_xpath)
    class_list = source_code.xpath(vehicle_class_xpath)
    driv_num = source_code.xpath(driving_num_xpath)

    # print(tree[0].text_content())

    for i in range(len(name_list)):
        final_data[0].append(name_list[i].text_content())
        final_data[1].append(issue_list[i].text_content())
        final_data[2].append(expiry_list[i].text_content())
        final_data[3].append(class_list[i].text_content())
        final_data[4].append(driv_num[i].text_content())

    output_df = pd.DataFrame(final_data)
    output_df.to_csv("output.csv", index=True)


# response = start(data)
#
# while response.status_code != 200:
#     start(data)


