import re

import requests
from bs4 import BeautifulSoup

from algo import MinPrice, MaxRating, MaxSold


class Search:

    def __init__(self, query):
        self.__query = query.lower()
        self.__url = 'https://plati.market/search/' + self.__query
        self.__result_count = 0

    def __get_response(self):  # получаем start_page и last_page или None
        response = requests.get(self.__url)
        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            self.__pages = soup.find_all('div', class_='pages_nav')[-1]
        except IndexError:
            return None
        else:
            self.__start_page = 1  # стартовая страница
            self.__last_page = (int([x.rstrip() for x in self.__pages.text.split('...')][-1])
                                if len(self.__pages.text.split()) > 4
                                else int(self.__pages.text.split()[-1][-1]))  # последняя страница

            return True

    def __raw_results(self):  # получаем список элементов

        raw_results = []

        for page in range(self.__start_page, self.__last_page + 1):
            url = f'{self.__url}?id={page}'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            raw = soup.find_all('li', class_='shadow')

            for i in raw:
                ol = i.find('ol').find_all('li')  # список ol

                name = i.h1.a.text.strip()
                link = 'https://plati.market' + i.h1.a.get('href')
                price = int(i.h1.span.text.split()[2])
                seller = ' '.join(ol[0].text.split()[1:-2]).replace(',', '')
                rating = float((ol[0].text.split()[-1]).replace(',', '.'))
                sales = int(ol[1].text.split()[1][:-1]) if ol[1].text.split()[1][:-1].isnumeric() else 0

                name_for_re = name.lower().replace('™', '')

                # поиск по split query
                if all([re.findall(fr'\b{x}\b', name_for_re.lower()) for x in self.__query.split()]):
                    raw_results.append([name, link, price, seller, rating, sales])

                # поиск по query
                # if re.findall(fr'\b{self.__query}\b', name_for_re):
                #     raw_results.append([name, link, price, seller, rating, sales])

                self.__result_count = len(raw_results)

        return raw_results

    def __get_min_max(self, raw_results):  # находим 3 элемента

        sorted_results = [
            ('min_price', MinPrice(raw_results).get_min_price()),
            ('max_rating', MaxRating(raw_results).get_max_rating()),
            ('max_sold', MaxSold(raw_results).get_max_sold())
        ]

        return sorted_results

    def __duplicates_search(self, sorted_results):  # ищем повторы
        results = []

        for i in range(len(sorted_results)):
            for j in range(i + 1, len(sorted_results)):
                if sorted_results[i][1] == sorted_results[j][1]:
                    results.append((sorted_results[i][0] + '_' + sorted_results[j][0], sorted_results[i][1]))

        if results:
            return results
        else:
            return sorted_results

    def __f_string_result(self, results):  # преобразуем в f-строки
        results_f_string = []

        if len(results) < 3:
            if results[0][0] == 'best_result':  # если остался только один элемент
                best_result = (
                    f'<b>Лучший результат:</b>'
                    f'\n<b>Название:</b> {results[0][0]}'
                    f'\n<b>Цена: {results[0][2]}</b> ₽'
                    f'\n<b>Продавец:</b> {results[0][3]}'
                    f'\n<b>Рейтинг: {results[0][4]}</b>'
                    f'\n<b>Продано: {results[0][5]}</b>'
                    f'\n<b>Ссылка:</b> {results[0][1]}'
                )
                results_f_string.append(best_result)
                return results_f_string
            else:  # если элементов < 3
                for i in results:
                    only_one_result = (
                        f'\n<b>Название:</b> {i[0]}'
                        f'\n<b>Цена:</b> {i[2]} ₽'
                        f'\n<b>Продавец:</b> {i[3]}'
                        f'\n<b>Рейтинг:</b> {i[4]}'
                        f'\n<b>Продано:</b> {i[5]}'
                        f'\n<b>Ссылка:</b> {i[1]}'
                    )
                    results_f_string.append(only_one_result)

                return results_f_string

        else:
            for i in results:
                if i[0] == 'min_price_max_rating' or i[0] == 'max_rating_min_price':
                    min_price_max_rating = (
                        f'<b>С минимальной ценой и максимальным рейтингом:</b>\n'
                        f'\n<b>Название:</b> {i[1][0]}'
                        f'\n<b>Цена: {i[1][2]}</b> ₽'
                        f'\n<b>Продавец:</b> {i[1][3]}'
                        f'\n<b>Рейтинг: {i[1][4]}</b>'
                        f'\n<b>Продано:</b> {i[1][5]}'
                        f'\n<b>Ссылка:</b> {i[1][1]}'
                    )
                    results_f_string.append(min_price_max_rating)

                elif i[0] == 'min_price_max_sold' or i[0] == 'max_sold_min_price':
                    min_price_max_sold = (
                        f'<b>С минимальной ценой и максимальным числом продаж:</b>\n'
                        f'\n<b>Название:</b> {i[1][0]}'
                        f'\n<b>Цена: {i[1][2]}</b> ₽'
                        f'\n<b>Продавец:</b> {i[1][3]}'
                        f'\n<b>Рейтинг:</b> {i[1][4]}'
                        f'\n<b>Продано: {i[1][5]}</b>'
                        f'\n<b>Ссылка:</b> {i[1][1]}'
                    )
                    results_f_string.append(min_price_max_sold)

                elif i[0] == 'max_rating_max_sold' or i[0] == 'max_sold_max_rating':
                    max_rating_max_sold = (
                        f'<b>С максимальным рейтингом и максимальным числом продаж:</b>\n'
                        f'\n<b>Название:</b> {i[1][0]}'
                        f'\n<b>Цена: {i[1][2]}</b> ₽'
                        f'\n<b>Продавец:</b> {i[1][3]}'
                        f'\n<b>Рейтинг:</b> {i[1][4]}'
                        f'\n<b>Продано: {i[1][5]}</b>'
                        f'\n<b>Ссылка:</b> {i[1][1]}'
                    )
                    results_f_string.append(max_rating_max_sold)

                elif i[0] == 'min_price':
                    min_price = (
                        f'<b>С минимальной ценой:</b>\n'
                        f'\n<b>Название:</b> {i[1][0]}'
                        f'\n<b>Цена: {i[1][2]}</b> ₽'
                        f'\n<b>Продавец:</b> {i[1][3]}'
                        f'\n<b>Рейтинг:</b> {i[1][4]}'
                        f'\n<b>Продано:</b> {i[1][5]}'
                        f'\n<b>Ссылка:</b> {i[1][1]}'
                    )
                    results_f_string.append(min_price)

                elif i[0] == 'max_rating':
                    max_rating = (
                        f'<b>С максимальным рейтингом:</b>\n'
                        f'\n<b>Название:</b> {i[1][0]}'
                        f'\n<b>Цена:</b> {i[1][2]} ₽'
                        f'\n<b>Продавец:</b> {i[1][3]}'
                        f'\n<b>Рейтинг: {i[1][4]}</b>'
                        f'\n<b>Продано:</b> {i[1][5]}'
                        f'\n<b>Ссылка:</b> {i[1][1]}'
                    )
                    results_f_string.append(max_rating)

                elif i[0] == 'max_sold':
                    max_sold = (
                        f'<b>С максимальным числом продаж:</b>\n'
                        f'\n<b>Название:</b> {i[1][0]}'
                        f'\n<b>Цена:</b> {i[1][2]} ₽'
                        f'\n<b>Продавец:</b> {i[1][3]}'
                        f'\n<b>Рейтинг:</b> {i[1][4]}'
                        f'\n<b>Продано: {i[1][5]}</b>'
                        f'\n<b>Ссылка:</b> {i[1][1]}'
                    )
                    results_f_string.append(max_sold)

            return results_f_string

    def get_result(self):  # получаем результат (основной метод)
        if self.__get_response() is None:
            return None

        else:
            raw_results = self.__raw_results()
            if self.__result_count == 0:
                return None

            elif len(raw_results) <= 3:  # если элементов <= 3, возвращаем результат без сортировки
                only_one_f_string = self.__f_string_result(raw_results)
                only_one_f_string.append(str(self.__result_count))

                return only_one_f_string

            else:  # если элементов > 3, сортируем
                sorted_result = self.__get_min_max(raw_results)
                best_result = list(set(tuple(x[1]) for x in sorted_result))  # список неповторяющихся элементов

                if len(best_result) == 1:  # если set вернул только один элемент
                    best_result = ('best_result', best_result)
                    best_result_f_string = self.__f_string_result(best_result)
                    best_result_f_string.append(str(self.__result_count))

                    return best_result_f_string

                else:  # если set вернул > 1 элемента
                    results = self.__duplicates_search(sorted_result)
                    results_f_string = self.__f_string_result(results)
                    results_f_string.append(str(self.__result_count))

                    return results_f_string
