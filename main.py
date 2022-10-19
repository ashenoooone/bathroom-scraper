import requests
from bs4 import BeautifulSoup
import csv
from fake_useragent import UserAgent

link_1 = "https://ntbathroom.ru/catalog/akrilovye-vanny/"
link_2 = "https://ntbathroom.ru/catalog/vanny-iz-iskusstvennogo-kamnya/"
ua = UserAgent()


def collect_data(pages):
    for page in pages:
        headers = {
            "user-agent": f"{ua.random}",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://www.fl.ru/",
            "Connection": "keep-alive",
        }
        r = requests.get(page, headers=headers)
        src = r.text
        soup = BeautifulSoup(src, "lxml")
        cards = soup.find_all("div", class_="products__item")
        res = []
        for card in cards:
            product_title = card.find("div", class_="product-tile__name").text
            product_price = card.find("div", class_="product-tile__price").text.replace("ь", "р/")
            product_link = f"https://ntbathroom.ru" \
                           f"{card.find('a', class_='product-tile__detail').get('href')}"
            res.append({
                "title": product_title,
                "price": product_price,
                "link": product_link
            })

        with open(f"res/{page.split('/')[-2]}.csv", "w", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Название", "Цена", "Ссылка"])
            for tv in res:
                writer.writerow([tv.get("title"), tv.get("price"), tv.get("link")])


def main():
    collect_data([link_1, link_2])


if __name__ == '__main__':
    main()
