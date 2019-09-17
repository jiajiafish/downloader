from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json
from pprint import pprint
def get_redurection_chain(url):
    """
    Given a url, return the urls in redirection chain and the length of the redirection chain.
    The redirection chain will be checked using selenium driven chrome browser and retrieved from
    browser log.

    :param url: the url that will be checked.
    :return: (
        length of redirection chain,
        a list of the urls in the redirection ordered based on the sequence they are visited,
    )
    """
    # landing_urls record origins->url->other intermedia urls->final_url
    landing_urls = list()
    landing_urls.append(url)

    curr_url = url

    capabilities = DesiredCapabilities.CHROME
    capabilities['loggingPrefs'] = {
        'performance': 'ALL',
    }
    
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('headless')

    driver = webdriver.Chrome(
        desired_capabilities=capabilities,
        chrome_options=options,
    )
    pprint(capabilities)
    a= driver.get(url)
    pprint(a)
    pprint(driver.get_log("client"))
    # for log in driver.get_log('performance'):
    #     log_entry = json.loads(log['message'])

    #     if 'redirectResponse' not in log_entry['message']['params']:
    #         continue
    #     if log_entry['message']['params']['redirectResponse']['url'] == curr_url:
    #         redirect_url = log_entry['message']['params']['request']['url']
    #         landing_urls.append(redirect_url)
    #         curr_url = redirect_url

    # driver.close()

    # return len(landing_urls), landing_urls

if __name__ == '__main__':
    get_redurection_chain('https://www.baidu.com/')