import random


class MinPrice:  # поиск минимальной цены
    def __init__(self, lst):
        self.lst = lst
        self.min_price = 0
        self.max_rating = 0
        self.max_sold = 0

    def __bubble_sort(self):  # пузырьковая сортировка (asc)
        flag = True

        while flag:
            flag = False
            for i in range(len(self.lst) - 1):
                if self.lst[i][2] > self.lst[i + 1][2]:
                    self.lst[i], self.lst[i + 1] = self.lst[i + 1], self.lst[i]
                    flag = True

        self.min_price = self.lst[0][2]  # min цена

        return self.lst

    def _same_items(self, field) -> list:  # ищем товары с одинаковой ценой
        ind = 0
        ind_name = ''

        if field == 'min_price':
            ind = 2
            ind_name = self.min_price
        elif field == 'max_rating':
            ind = 4
            ind_name = self.max_rating
        elif field == 'max_sold':
            ind = 5
            ind_name = self.max_sold

        same_price = []

        for i in self.lst:
            if i[ind] == ind_name:
                same_price.append(i)

        return same_price

    def _max_rating_if_same_items(self,
                                  same_items):  # находим max рейтинг продавца, если есть товары с одинаковой ценой
        ind = 0
        max_ = same_items[0][4]
        for i in range(len(same_items)):
            if same_items[i][4] > max_:
                max_ = same_items[i][4]
                ind = i

        return same_items[ind]

    def get_min_price(self):
        sorted_lst = self.__bubble_sort()
        same_price = self._same_items('min_price')

        if len(same_price) > 1:
            result = self._max_rating_if_same_items(same_price)
            return result
        else:
            return same_price[0]


class MaxRating(MinPrice):  # поиск max рейтинга

    def __selection_sort(self):  # сортировка выбором (desc)
        for item in self.lst:
            for i in range(len(self.lst)):
                min_ = i
                for j in range(i + 1, len(self.lst)):
                    if self.lst[j][4] > self.lst[min_][4]:
                        min_ = j
                self.lst[i], self.lst[min_] = self.lst[min_], self.lst[i]

        self.max_rating = self.lst[0][4]  # max рейтинг

        return self.lst

    def _min_price_if_same_items(self,
                                 same_items):  # находим min цену товара, если есть продавцы с одинаковым рейтингом
        ind = 0
        min_ = same_items[0][2]
        for i, v in enumerate(same_items):
            if v[2] < min_:
                min_ = v[2]
                ind = i

        return same_items[ind]

    def get_max_rating(self):
        sorted_lst = self.__selection_sort()
        same_rating = self._same_items('max_rating')

        if len(same_rating) > 1:
            result = self._min_price_if_same_items(same_rating)
            return result
        else:
            return same_rating[0]


class MaxSold(MaxRating):  # поиск max числа продаж

    def __quick_sort(self):  # быстрая сортировка (asc)
        def _quicksort(lst, start, end):
            if start >= end:
                return lst

            x = lst[random.randint(start, end)][5]
            low, high = start, end

            while low <= high:
                while lst[low][5] < x:
                    low += 1
                while lst[high][5] > x:
                    high -= 1

                if low <= high:
                    lst[low], lst[high] = lst[high], lst[low]
                    low += 1
                    high -= 1

            _quicksort(lst, start, high)
            _quicksort(lst, low, end)

            return lst

        self.lst = _quicksort(self.lst, 0, len(self.lst) - 1)

        self.max_sold = self.lst[-1][5]  # max число продаж

        return self.lst

    def get_max_sold(self):
        sorted_list = self.__quick_sort()
        same_sold = self._same_items('max_sold')

        if len(same_sold) > 1:
            result = self._min_price_if_same_items(same_sold)
            return result
        else:
            return same_sold[0]
