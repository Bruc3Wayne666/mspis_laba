import requests
from bs4 import BeautifulSoup


def get_search_results(query):
    url = f"https://www.google.com/search?q={query}&num=30"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        print("Ошибка при получении страницы:", response.status_code)
        return None


def parse_results(html):
    soup = BeautifulSoup(html, 'html.parser')
    results = []

    search_results = soup.find_all('div', class_='g')

    for index, result in enumerate(search_results):
        if index >= 20:
            break

        title = result.find('h3')
        link = result.find('a')['href']

        if title and link:
            results.append({
                'page': 1 + (index // 10),
                'url': link,
                'title': title.text
            })

    return results


def main():
    html = get_search_results(input("Введите поисковый запрос: "))

    if html:
        results = parse_results(html)
        print(*results, sep='\n')


main()