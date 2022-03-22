from bs4 import BeautifulSoup
import requests


# avito.ru listings parser #
def search_by_query_avito(query, city, num_listings=10):
    domain = "https://www.avito.ru"
    soup = BeautifulSoup(requests.get(f"{domain}/{city}?q={query}", verify=False).text, "lxml")  # soup of a page with listings
    listing_preview = soup.find_all("div", {"data-marker": "item"})  # previews of listings
    data = []
    for i in range(num_listings):
        if i >= len(listing_preview):
            break
        else:
            title = listing_preview[i].find("a", {"data-marker": "item-title"}).find("h3").getText(' ')  # title of a listing
            price = listing_preview[i].find("span",
                                            {"class": "price-text-_YGDY text-text-LurtD text-size-s-BxGpL"}).getText()
            rel_link = listing_preview[i].find("a", {"data-marker": "item-title"})['href']  # relative link of a listing
            abs_link = f"{domain}{rel_link}"
            description = listing_preview[i].find("div", {"class": "iva-item-descriptionStep-C0ty1"}).getText(' ')
            img_link = listing_preview[i].find("img", {"class": "photo-slider-image-YqMGj"})['src']
            data.append({"title": title, "price": price, "link": abs_link, "description": description, "img_link": img_link})

    return data


# youla.ru listings parser (WIP) #
def search_by_query_youla(query, city, num_listings=10):
    domain = "https://youla.ru"
    soup = BeautifulSoup(requests.get(f"{domain}/{city}?q={query}", verify=False).text, "html.parser")  # soup of a page with listings

    listing_preview = soup.find_all('div')  # previews of listings

    print(soup)
    data = []
    for i in range(num_listings):
        if i >= len(listing_preview):
            break
        else:
            pass
            # title = listing_preview[i].find("a", {"data-marker": "item-title"}).find("h3").getText(' ')  # title of a listing
            # rel_link = listing_preview[i].find("a", {"data-marker": "item-title"})['href']  # relative link of a listing
            # abs_link = f"{domain}{rel_link}"
            # data.append({"title": title, "link": abs_link})

    return data


def search_by_query(sites, query, city, num_listings):

    for site in sites:
        if site == "avito":
            return search_by_query_avito(query, city, num_listings)
        elif site == "youla":
            pass

