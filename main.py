import requests
import re

def extract_article_data(article_url):
    response = requests.get(article_url)
    response.encoding = 'utf-8'
    html_content = response.text

    # Wyrażenie regularne dla wewnętrznych linków (linki zaczynające się od "/wiki/" bez ujednoznacznienia)
    internal_links = re.findall(r'href="/wiki/([^":#]+?)"', html_content)
    article_links = [link.replace('_', ' ') for link in internal_links[:5]]  # Pierwsze 5 linków wewnętrznych

    # Wyrażenie regularne dla obrazów
    image_urls = re.findall(r'src="(//upload\.wikimedia\.org/[^"]+)"', html_content)[:3]

    # Wyrażenie regularne dla linków zewnętrznych
    external_urls = re.findall(r'href="(https?://[^"]+)" class="external"', html_content)[:3]

    # Wyrażenie regularne dla kategorii (zakładam, że są w divie 'mw-normal-catlinks')
    categories = re.findall(r'<div id="mw-normal-catlinks".*?>(.*?)</div>', html_content, re.DOTALL)
    category_links = re.findall(r'title="Kategoria:[^"]+">([^<]+)', categories[0]) if categories else []

    # Formatowanie linków wewnętrznych - dodajemy "(ujednoznacznienie)", jeśli potrzeba
    formatted_links = [
        f"{link} (ujednoznacznienie)" if "ujednoznacznienie" in link.lower() else link for link in article_links
    ]
    formatted_categories = [category.strip() for category in category_links]

    return {
        "links": formatted_links or [""],
        "images": image_urls or [""],
        "external_urls": external_urls or [""],
        "categories": formatted_categories or [""]
    }

def main():
    category_name = input().strip()
    category_url = f"https://pl.wikipedia.org/wiki/Kategoria:{category_name.replace(' ', '_')}"
    response = requests.get(category_url)
    response.encoding = 'utf-8'
    html_content = response.text

    # Wyszukiwanie linków do pierwszych dwóch artykułów w kategorii
    article_urls = re.findall(r'href="(/wiki/[^":#]+?)"', html_content)[:2]
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