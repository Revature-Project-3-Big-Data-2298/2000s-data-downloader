import requests
from urllib.parse import urljoin
import urllib.request
from bs4 import BeautifulSoup
from zipfile import ZipFile
import os

URL_LIST = ["https://www2.census.gov/census_2000/datasets/redistricting_file--pl_94-171/"]

def files2000() -> list:
    print(f"Scraping {URL_LIST[0]} for states...")
    files = []
    #get the page, pass it into beautiful soup
    response = requests.get(URL_LIST[0])
    soup = BeautifulSoup(response.text, 'html.parser')
    #find all links using soup
    links = soup.find_all('a')
    for link in links[9:61]:
        print(f"Scraping {link["href"]} for download file...")
        #for each link, check it for links
        sub_url = urljoin(URL_LIST[0], link["href"])
        sub_response = requests.get(sub_url)
        sub_soup = BeautifulSoup(sub_response.text, 'html.parser')
        sub_links = sub_soup.find_all('a')
        #for each sub link we need to find our files
        for sub_link in sub_links: 
            try: #some anchor tags do not have an href, hence the try
                href = sub_link["href"]
                if "0001" in href: #look for "0001" in the name of the file and append it to files
                    files.append(urljoin(sub_url, href))
                    print(f"File found -> {href}")
            except:
                pass #if no href: it is not our file. we can pass
    return files

def downloadList(files:list):
    print(f'Downloading {len(files)} files...')
    i = 1
    for file in files:
        print(f"{file} -> Downloading({i}/{len(files)})...")
        i += 1
        #for file in files list we find the filename by splitting, then request the file using urllib.request.urlretrieve
        filename = file.split('/')[-1]
        urllib.request.urlretrieve(file, filename)
        #then extract the file using ZipFile
        with ZipFile(filename, 'r') as zip_file:
            print(f"{file} -> Extracting...")
            zip_file.extractall()
        #then delete the zip file after it is extracted
        os.remove(filename)
    print('All Downloads Complete!')

if __name__ == "__main__": downloadList(files2000())