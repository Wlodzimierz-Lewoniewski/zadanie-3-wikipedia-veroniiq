import requests
from bs4 import BeautifulSoup


def extract_article_data(article_url):
    response = requests.get(article_url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Ekstrakcja odnośników wewnętrznych do innych artykułów
    links = soup.select('a[href^="/wiki/"]')
    article_links = [link.get_text() for link in links if ':' not in link['href']][:5]

    # Ekstrakcja URL-i obrazków
    images = soup.select('img')
    image_urls = ["https:" + img['src'] for img in images if 'src' in img.attrs][:3]

    # Ekstrakcja URL-i źródeł zewnętrznych
    external_links = soup.select('a.external')
    external_urls = [link['href'] for link in external_links if 'href' in link.attrs][:3]

    # Ekstrakcja nazw kategorii
    categories = soup.select('#mw-normal-catlinks ul li a')
    category_names = [category.get_text() for category in categories][:3]

    return {
        "links": article_links,
        "images": image_urls,
        "external_urls": external_urls,
        "categories": category_names
    }


def main():
    # Pobranie kategorii od użytkownika
    category_name = input().strip()
    category_url = f"https://pl.wikipedia.org/wiki/Kategoria:{category_name.replace(' ', '_')}"

    # Pobranie listy artykułów z kategorii
    response = requests.get(category_url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Pobieranie linków do pierwszych dwóch artykułów z kategorii
    article_links = ["https://pl.wikipedia.org" + a['href'] for a in soup.select('.mw-category a')][:2]

    results = []

    for article_url in article_links:
        data = extract_article_data(article_url)
        # Formatowanie wyników dla każdego artykułu
        results.append(
            f"{' | '.join(data['links']) or ''}\n"
            f"{' | '.join(data['images']) or ''}\n"
            f"{' | '.join(data['external_urls']) or ''}\n"
            f"{' | '.join(data['categories']) or ''}"
        )

    # Wyświetlenie wyników w odpowiednim formacie dla testów
    print("\n".join(results))

if __name__ == "__main__":
    main()