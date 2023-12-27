import re
import time

import requests

from algo import MinPrice, MaxRating, MaxSold


class SearchAPI:
    def __init__(self, query):
        self.__query = query
        self.__url = f'https://plati.io/api/search.ashx?query={query}&visibleOnly=True&response=json'
        self.__result_count = 0

    def __get_response(self):
        if requests.get(self.__url).status_code == 200:
            response = requests.get(self.__url).json()  # ответ в json
            if response['total'] == 0:
                return None
            else:
                self.__result_count = response['total']  # общее кол-во элементов

            return response

        else:
            return None

    def __raw_results(self, response):
        raw_results = []

        for i in response['items']:
            name = i['name']
            link = i['url']
            price = i['price_rur']
            seller = i['seller_name']
            rating = i['seller_rating']
            sales = i['numsold'] if i['numsold'] > 0 else 0

            if self.__result_count <= 3:
                raw_results.append([name, link, price, seller, rating, sales])
            else:
                name_for_re = name.lower().replace('™', '')

                # поиск по split query
                if all([re.findall(fr'\b{x}\b', name_for_re.lower()) for x in self.__query.lower().split()]):
                    raw_results.append([name, link, price, seller, rating, sales])

                # поиск по query
                # if re.findall(fr'\b{self.__query.lower()}\b', name_for_re):
                #     raw_results.append([name, link, price, seller, rating, sales])

        if len(raw_results) >= 1:
            return raw_results
        else:
            return None

    def __get_min_max(self, raw_results):

        sorted_results = [
            ('min_price', MinPrice(raw_results).get_min_price()),
            ('max_rating', MaxRating(raw_results).get_max_rating()),
            ('max_sold', MaxSold(raw_results).get_max_sold())
        ]

        return sorted_results

    def __duplicates_search(self, sorted_results):
        results = []
        for i in range(len(sorted_results)):
            for j in range(i + 1, len(sorted_results)):
                if sorted_results[i][1] == sorted_results[j][1]:
                    results.append((sorted_results[i][0] + '_' + sorted_results[j][0], sorted_results[i][1]))
                    del sorted_results[i], sorted_results[i]
                    break
        if results:
            results.append(*sorted_results)
            return results
        else:
            return sorted_results

    def __f_string_result(self, results):
        results_f_string = []

        if results[0] == 'best_result':  # если остался только один элемент
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
                else:
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

    def get_result(self):
        time.sleep(1)  # от дудоса

        response = self.__get_response()

        if response is None:
            return None

        else:
            raw_results = self.__raw_results(response)

            if raw_results is None or self.__result_count == 0:
                return None

            if len(raw_results) <= 3:  # если элементов <= 3, возвращаем результат без сортировки
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
