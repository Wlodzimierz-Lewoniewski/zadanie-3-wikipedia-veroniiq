import requests
import re
import urllib.parse

def extract_article_data(article_url):
    response = requests.get(article_url)
    response.encoding = 'utf-8'
    html_content = response.text

    # Wyrażenie regularne dla wewnętrznych linków (linki zaczynające się od "/wiki/" bez ujednoznacznienia)
    article_links = []
    excluded_namespaces = (
        "Kategoria:", "Plik:", "Wikipedia:", "Pomoc:", "Portal:",
        "Wikipedysta:", "MediaWiki:", "Szablon:", "Moduł:",
        "Specjalna:", "Media:"
    )

    # Wyrażenie regularne do szukania linków wewnętrznych "/wiki/..." w artykule
    for link in re.findall(r'<a href="/wiki/([^":#]+)"', html_content):
        # Filtracja przestrzeni nazw poprzez sprawdzenie, czy link nie zawiera prefiksu z listy wykluczeń
        if not any(link.startswith(namespace) for namespace in excluded_namespaces):
            # Dekodowanie URL i zamiana "_" na spacje
            title = urllib.parse.unquote(link).replace('_', ' ')
            article_links.append(title)
            # Przerwanie, gdy mamy 5 linków
            if len(article_links) >= 5:
                break

    # Wyrażenie regularne dla obrazów
    image_urls = re.findall(r'src="(//upload\.wikimedia\.org/[^"]+)"', html_content)[:3]

    # Wyrażenie regularne dla linków zewnętrznych
    external_urls = re.findall(r'class="reference-text">.*?<a rel="nofollow" class="external text" href="(https?://[^"]+)"', html_content, re.DOTALL)[:3]

    # Wyrażenie regularne dla kategorii
    categories = re.findall(r'<div id="mw-normal-catlinks".*?>(.*?)</div>', html_content, re.DOTALL)
    category_links = re.findall(r'title="Kategoria:[^"]+">([^<]+)', categories[0]) if categories else []
    category_links = category_links[:3]

    return {
        "links": article_links or [""],
        "images": image_urls or [""],
        "external_urls": external_urls or [""],
        "categories": category_links or [""]
    }

def main():
    category_name = input().strip()
    category_url = f"https://pl.wikipedia.org/wiki/Kategoria:{category_name.replace(' ', '_')}"
    response = requests.get(category_url)
    response.encoding = 'utf-8'
    html_content = response.text

    # Wyszukiwanie linków do pierwszych dwóch artykułów w kategorii
    article_urls = re.findall(r'<li><a href="(/wiki/[^":#]+?)"', html_content)[:2]
    full_article_urls = ["https://pl.wikipedia.org" + url for url in article_urls]

    results = []

    for article_url in full_article_urls:
        data = extract_article_data(article_url)

        # Formatowanie wyników dla obrazów i linków zewnętrznych
        formatted_data = (
            f"{' | '.join(data['links'])}\n"
            f"{' | '.join(data['images'])}\n"
            f"{' | '.join(data['external_urls'])}\n"
            f"{' | '.join(data['categories'])}"
        )
        results.append(formatted_data)

    # Wyświetlanie wyników
    print("\n\n".join(results))

if __name__ == "__main__":
    main()