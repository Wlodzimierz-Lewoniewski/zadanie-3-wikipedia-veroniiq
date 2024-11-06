import requests
from bs4 import BeautifulSoup

def extract_article_data(article_url):
    response = requests.get(article_url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.content, "html.parser")

    links = soup.select('a[href^="/wiki/"]')
    article_links = [link.get_text() for link in links if ':' not in link['href']][:5]

    # Pobieranie obrazów z formatowaniem zgodnie z wymaganiami
    images = soup.select('img')
    image_urls = [
        "//" + img['src'] for img in images if 'src' in img.attrs
    ][:3]

    # Pobieranie linków zewnętrznych z formatowaniem zgodnie z wymaganiami
    external_links = soup.select('a.external')
    external_urls = [
        link['href'] for link in external_links if 'href' in link.attrs
    ][:3]

    # Pobieranie kategorii
    categories = soup.select('#mw-normal-catlinks ul li a')
    category_names = [category.get_text(strip=True) for category in categories][:3]

    # Formatowanie linków wewnętrznych
    formatted_links = [
        f"{link} (ujednoznaczniczenie)" if "ujednoznacznienie" in link.lower() else link for link in article_links
    ]

    return {
        "links": formatted_links or [""],
        "images": image_urls or [""],
        "external_urls": external_urls or [""],
        "categories": category_names or [""]
    }

def main():
    category_name = input().strip()
    category_url = f"https://pl.wikipedia.org/wiki/Kategoria:{category_name.replace(' ', '_')}"
    response = requests.get(category_url)
    response.encoding = 'utf-8'

    soup = BeautifulSoup(response.content, "html.parser")

    article_links = ["https://pl.wikipedia.org" + a['href'] for a in soup.select('.mw-category a')][:2]

    results = []

    for article_url in article_links:
        data = extract_article_data(article_url)

        # Formatowanie wyników dla obrazów i linków zewnętrznych
        formatted_data = (
            f"{' | '.join(data['links'])}\n"
            f"{' | '.join(data['images'])}\n"
            f"{' | '.join(data['external_urls'])}\n"
            f"{' | '.join(data['categories'])}"
        )
        results.append(formatted_data)

    print("\n".join(results))

if __name__ == "__main__":
    main()