import argparse
import csv
import os
import requests
import utils
from bs4 import BeautifulSoup
from urllib.parse import urljoin

base_url = "http://www.hitparadeitalia.it/hp_weeks/hpw_{}.htm"


def get_all_urls(url, logger):
    try:
        page = requests.get(url)
    except Exception as e:
        logger.error(e)
        return []
    urlList = []
    try:
        soup = BeautifulSoup(page.text, "html.parser")
        soup.prettify()
        for anchor in soup.findAll('a', href=True):
            if 'http://' not in anchor['href']:
                if urljoin(url, anchor['href']) not in urlList:
                    urlList.append(urljoin(url, anchor['href']))
            else:
                if anchor['href'] not in urlList:
                    urlList.append(anchor['href'])

        length = len(urlList)

        return urlList
    except Exception as e:
        logger.error(e)


def listAllUrl(urls):
    for x in urls:
        print(x)
        urls.remove(x)
        urls_tmp = get_all_urls(x)
        for y in urls_tmp:
            urls.append(y)


def from_table_to_csv(url):
    try:
        page = requests.get(url)
    except Exception as e:
        logger.error(e)
        return []
    try:
        soup = BeautifulSoup(page.text, "lxml")
        soup.prettify()
        table = soup.find_all("table")[1]
        # python3 just use th.text
        headers = [th.text.encode("utf-8") for th in table.select("tr th")]
        filename = url.rsplit('/', 1)[-1]
        with open("data/{}_out.csv".format(filename), "w", encoding='utf-8') as f:
            wr = csv.writer(f)
            wr.writerow(headers)
            wr.writerows([[td.text.strip() for td in row.find_all("td")] for row in table.select("tr + tr")])
    except Exception as e:
        logger.error(e)
        table = soup.find_all("li")
        filename = url.rsplit('/', 1)[-1]
        headers = []
        with open("data/{}_out.csv".format(filename), "w", encoding='utf-8') as f:
            wr = csv.writer(f)
            wr.writerow(headers)
            i = 1
            for song in table:
                row = [i, i]
                row.extend([t.strip() for t in song.text.strip().split('-')])
                wr.writerow(row)
                i += 1
            # f.write("\n".join(map(str, [row.text.strip() for row in table])))


if __name__ == "__main__":
    # Getting the boot_configuration as argument
    parser = argparse.ArgumentParser(
        description='Script that get all the hit rankings for weeks and write on \"data\" folder')
    parser.add_argument('-s', '--start', type=int, help='start year. Default is %(default)',
                        default=1959)
    parser.add_argument('-e', '--end', type=int, help='end year NOT inclusive. Default is %(default)',
                        default=2008)
    parser.add_argument('-d', '--debug', default=False, action='store_true',
                        help='it will activate DEBUG severity level and it save and create folder in example')
    args = parser.parse_args()
    start = args.start
    end = args.end
    debug_mode = args.debug
    logger = utils.setup_logger(os.path.basename(__file__))
    logger.info("Start script")
    web_pages = [base_url.format(str(year)) for year in range(start, end, 1)]
    for web_page in web_pages:
        urls = get_all_urls(web_page, logger)
        for url in urls:
            from_table_to_csv(url)
    logger.info("End")