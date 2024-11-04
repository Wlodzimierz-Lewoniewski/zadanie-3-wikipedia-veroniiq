import requests
from bs4 import BeautifulSoup


def extract_article_data(article_url):
    response = requests.get(article_url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.content, "html.parser")

    # Ekstrakcja nazw odnośników do innych artykułów (wewnętrznych) i ich treści
    links = soup.select('a[href^="/wiki/"]')
    article_links = []

    for link in links:
        if ':' not in link['href']:
            text = link.get_text(strip=True)
            if text:
                article_links.append(text)
        if len(article_links) >= 5:
            break

    # Ekstrakcja URL-i obrazków
    images = soup.select('img')
    image_urls = ["https:" + img['src'] for img in images if 'src' in img.attrs][:3]

    # Ekstrakcja URL-i źródeł zewnętrznych
    external_links = soup.select('a.external')
    external_urls = [link['href'] for link in external_links if 'href' in link.attrs][:3]

    # Ekstrakcja nazw kategorii przypisanych do artykułu
    categories = soup.select('#mw-normal-catlinks ul li a')
    category_names = [category.get_text(strip=True) for category in categories][:3]

    # Dodanie "(ujednoznacznienie)" dla odpowiednich nazw
    formatted_links = [f"{link} (ujednoznacznienie)" if "ujednoznacznienie" in link.lower() else link for link in
                       article_links]

    return {
        "links": formatted_links or [""],
        "images": image_urls or [""],
        "external_urls": external_urls or [""],
        "categories": category_names or [""]
    }


def main():
    # Pobranie nazwy kategorii od użytkownika
    category_name = input("Podaj nazwę kategorii na Wikipedii: ")

    category_url = f"https://pl.wikipedia.org/wiki/Kategoria:{category_name.replace(' ', '_')}"
    response = requests.get(category_url)
    response.encoding = 'utf-8'

    if response.status_code != 200:
        print("Nie udało się pobrać kategorii. Sprawdź, czy kategoria istnieje.")
        return

    soup = BeautifulSoup(response.content, "html.parser")

    # Pobieranie linków do pierwszych dwóch artykułów z kategorii
    article_links = ["https://pl.wikipedia.org" + a['href'] for a in soup.select('.mw-category a')][:2]

    results = []

    for article_url in article_links:
        data = extract_article_data(article_url)

        # Formatowanie wyników dla każdego artykułu z zachowaniem kolejności i formatu
        formatted_data = (
            f"{' | '.join(data['links'])}\n"
            f"{' | '.join(data['images'])}\n"
            f"{' | '.join(data['external_urls'])}\n"
            f"{' | '.join(data['categories'])}"
        )
        results.append(formatted_data)

    # Wyświetlenie wyników w odpowiednim formacie dla testów
    print("\n".join(results))

if __name__ == "__main__":
    main()