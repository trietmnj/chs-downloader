import requests
import argparse
from html.parser import HTMLParser
from bs4 import BeautifulSoup
from selenium import webdriver
from seleniumrequests import Firefox as WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

debug = True

study_encode = {
        "n": 1,
        }

links = {
        "study": "https://chs.erdc.dren.mil/Storm/CascadingGetStudies",
        "login": "https://chs.erdc.dren.mil/Login/LoginGuest",

        # query string params: level, extent, zoom, study
        # form data param: __RequestVerificationToken
        "mapping_points": "https://chs.erdc.dren.mil/Storm/GetMappingPoints?level=7&extent=-72.137498%2040.817117,-71.930817%2041.240314&zoom=11&study=5"
        }

def get_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Download CHS data")
    parser.add_argument(
        '-o',
        '--output_folder',
        nargs='+',
        help='Folder path i.e. where you can see "Data" and "Outputs" folder')
    return parser

def main(args: argparse.ArgumentParser) -> None:
    # cookies = {
    #     '_ga': 'GA1.2.889996012.1657855063',
    #     '__RequestVerificationToken': 'wCe1Hsbz7cJAUOa-7i84bXeYmO5LzJ8BY_VJd56dSkrsJWvQT0NqtghG7-4kNPBvXLrd22asHLHXzDTDaa_wylP0qXpohr6IDs3Cskr4PdY1',
    #     'PF': '71NszKageKAZCje1mpbVTMmjAEf9tfogC9DW4pclaFAV',
    #     'CacOnlyOpentoken': 'T1RLAQHMPIPlp-qJJ-o8OnCv541hl7blYRA-IscbKTPXNnAd3sjXnLK0AAEg_9M-27omyCzWIe74S-JxSfUjWXrI44mG9xg4uojc8Nhuqcd9fFp-6pJDx9Ym5nehzUkbZDfURXl6voLI4ZOWKCbE6qJbun6G0nSbspK7mMWP4r1zF_eOty04_XXTKIbub7BALzi4lgwh0aFbZZqCgagT8kVUo2UTVduZ_2S1Ue4XxyWEvyrXOOB673NZcQmrjF5XlxQLFnnmvZ0cbzrwRAtBxm_KrgSDWBiWL7Qx-THVpTWE_eORF4_s8ZDk7W62-xXq2ntqPDb1wwPmcouaLpIOT8dm_yPXwmnKRkObfCOh9m-FVwjfibAG-vYi3pv_P1ny3EGdApXPti0xkINS1pfcxC8-3RcvloVbRjLyH5ZooaNwdJ96rkkGecrEZVVV',
    #     '.ASPXAUTH': '3F2D955021F11485D5E8CB0F0BD90B38AE8EEB458CF31C2C500160EC3B28A824C575C0136FB901ED2DCED4C6279DAE8F46590F59483CC8D43AA204FD72741743F45CF95421AC20D8BC52C3CBD84251FB',
    # }

    # headers = {
    #     'authority': 'chs.erdc.dren.mil',
    #     'accept': '*/*',
    #     'accept-language': 'en-US,en;q=0.9',
    #     'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    #     # Requests sorts cookies= alphabetically
    #     # 'cookie': '_ga=GA1.2.889996012.1657855063; __RequestVerificationToken=wCe1Hsbz7cJAUOa-7i84bXeYmO5LzJ8BY_VJd56dSkrsJWvQT0NqtghG7-4kNPBvXLrd22asHLHXzDTDaa_wylP0qXpohr6IDs3Cskr4PdY1; PF=71NszKageKAZCje1mpbVTMmjAEf9tfogC9DW4pclaFAV; CacOnlyOpentoken=T1RLAQHMPIPlp-qJJ-o8OnCv541hl7blYRA-IscbKTPXNnAd3sjXnLK0AAEg_9M-27omyCzWIe74S-JxSfUjWXrI44mG9xg4uojc8Nhuqcd9fFp-6pJDx9Ym5nehzUkbZDfURXl6voLI4ZOWKCbE6qJbun6G0nSbspK7mMWP4r1zF_eOty04_XXTKIbub7BALzi4lgwh0aFbZZqCgagT8kVUo2UTVduZ_2S1Ue4XxyWEvyrXOOB673NZcQmrjF5XlxQLFnnmvZ0cbzrwRAtBxm_KrgSDWBiWL7Qx-THVpTWE_eORF4_s8ZDk7W62-xXq2ntqPDb1wwPmcouaLpIOT8dm_yPXwmnKRkObfCOh9m-FVwjfibAG-vYi3pv_P1ny3EGdApXPti0xkINS1pfcxC8-3RcvloVbRjLyH5ZooaNwdJ96rkkGecrEZVVV; .ASPXAUTH=3F2D955021F11485D5E8CB0F0BD90B38AE8EEB458CF31C2C500160EC3B28A824C575C0136FB901ED2DCED4C6279DAE8F46590F59483CC8D43AA204FD72741743F45CF95421AC20D8BC52C3CBD84251FB',
    #     'origin': 'https://chs.erdc.dren.mil',
    #     'referer': 'https://chs.erdc.dren.mil/Study/Index',
    #     'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    #     'sec-ch-ua-mobile': '?0',
    #     'sec-ch-ua-platform': '"Windows"',
    #     'sec-fetch-dest': 'empty',
    #     'sec-fetch-mode': 'cors',
    #     'sec-fetch-site': 'same-origin',
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    #     'x-requested-with': 'XMLHttpRequest',
    # }

    # data = {
    #     '__RequestVerificationToken': 'ZzN4Dq5b9enhLWtryvJewRFV1fHaEwJphvgqBtUCArqolv1zy6FwyClvxUCtEspZbG3EQHr7DCPi0AFBLxjKNDvGQVCM6mIvaWe-5INJHk01',
    # }
    # download_link = "https://chs.erdc.dren.mil/Study/SelectedSavePoints_DownloadGrid_DownloadSelected?study=5&fileids=390558,772190&includecsv=false&includeh5=true"
    # download_link = "https://chs.erdc.dren.mil/Study/GetMappingPoints?level=7&extent=-80.489013%2028.253501,-80.345161%2028.403697&zoom=12&study=6&projects=28,32,36" res = requests.post(url, cookies=cookies, headers=headers, data=data)
    # res = requests.post(download_link, cookies=cookies, headers=headers, data=data)
    # res = requests.post(download_link, cookies=cookies, headers=headers)
    # flag_login = is_login_page(res)

    options = Options()
    options.add_argument("--headless")
    # driver = webdriver.Firefox(options=options)
    driver = WebDriver()
    # driver.get(download_link)

    # if is_login_page(driver): continue_from_login(driver)

    driver.get(links["login"])

    token = ""
    map_link = "https://chs.erdc.dren.mil/Storm"
    print("Loading storm map")
    driver.get(map_link)

    token = parse_token(driver)

    # continuing on from login page
    if is_login_page(driver):
        if debug: print("Reached login page, continuing on...")
        continue_from_login(driver)
        print(token)

    # close down disclaimer prompt
    print("Closing disclaimer")
    disclaimer_x = driver.find_element(By.CLASS_NAME, "k-window-action")
    disclaimer_x.click()

    print("Loading points")
    # points_res = requests.post(links["mapping_points"], headers={"User-Agent": "Mozilla/5.0"}, data={"__RequestVerificationToken" : token})

    points = driver.request("POST", links["mapping_points"], data={"__RequestVerificationToken" : token})
    print(points.json())

    # file = "out/meta.json"
    # with open(file, "wb") as file:
    #     file.write(res.content)
    driver.quit()

def parse_token(d: WebDriver) -> str:
    elem = d.find_element(By.XPATH, "html/body/input")
    print(elem.get_attribute("value"))
    return elem.get_attribute("value")

def is_login_page(d: WebDriver) -> bool:
    """ Check whether page was rerouted to login """
    # test_phrase = "You are accessing a U.S. Government (USG) Information System (IS) that is provided for USG-authorized use only."
    # return test_phrase in r.text
    return "CHS - Login" in d.title

def continue_from_login(d: WebDriver) -> None:
    """ Take a response of a possible login page, parse and
    return verification token plus a no-domain redirect path """

    elem = d.find_element(By.XPATH, "html/body/div[3]/div[1]/div[3]/div/a")
    elem.click()
    # print(elem)

    # soup = BeautifulSoup(r.text, "html.parser")
    # token = soup.find("input", {"name": "__RequestVerificationToken"})
    # token = token["value"] if token is not None else ""
    # div_elem_with_child = soup.find("div", {"class": "panelx-login light-gray"}).find_child("a")
    # path = div_elem_with_child["href"] if div_elem_with_child else ""

    # return token, path


if __name__ == "__main__":
    args = get_args()
    main(args)
