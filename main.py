import requests
from bs4 import BeautifulSoup


def get_all_subcategories(soup_block):
    all_subcategories = []
    for sub_block in soup_block:
        try:
            sub_links = []
            for sub_link in sub_block.find("ul").find_all("li"):
                sub_links.append(sub_link.find("a").get("href"))
                # print(sub_link.find("a").get("href"))
            all_subcategories.append(sub_links)
        except AttributeError:
            all_subcategories.append([sub_block.find("a").get("href")])
    return all_subcategories

def check_for_subsub(link):
    if len(link.split("/")) <= 4: return [link]
    LINK = "https://stalenergo-96.ru"
    fullLink = LINK+link

    subsub_response = requests.get(fullLink).text
    subsub_soup = BeautifulSoup(subsub_response, "lxml")

    subsub_catalogue_block = subsub_soup.find("div", class_="left_col_content").find("li", class_="active")

    try:
        subsub_catalogue = subsub_catalogue_block.find("li", class_="active").find("ul")
    except AttributeError:
        subsub_catalogue = subsub_catalogue_block.find("ul")

    categories_link = []

    if subsub_catalogue:
        for i in subsub_catalogue.find_all("a"): categories_link.append(i.get("href"))
    else: categories_link.append(subsub_catalogue_block.find_all("a")[1].get("href"))

    return categories_link



def main():
    LINK = "https://stalenergo-96.ru"
    fullLink = LINK+"/produkcia/"

    response = requests.get(fullLink).text
    soup = BeautifulSoup(response, "lxml")
    cats_block = soup.find("div", class_="catalogue_content").find_all("div", class_="catalogue__item")

    all_subcategories = get_all_subcategories(cats_block)
    # print(*all_subcategories, sep="\n")

    all_links = []
    for cats in all_subcategories:
        for subcat in cats:
            links = check_for_subsub(subcat)
            if links not in all_links: all_links.append(links), print(*links, sep="\n")
    print(*all_links, sep="\n")

if __name__ == "__main__":
    main()