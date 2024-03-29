# Телеграм-бот [PlatiRu Bot](https://t.me/xPlatiRuBot) | [DockerHub](https://hub.docker.com/r/v2rg/plati-ru-bot)
- Бот осуществляет поиск по сайту plati.ru (plati.market)
- Выводит три варианта из найденного:
    - с минимальной ценой
    - с максимальным числом продаж
    - с максимальным рейтингом продавца
  ---
    - либо объединяет варианты, если они совпадают (цена+продажи, цена+рейтинг, продажи+рейтинг)
    - либо выводит только один вариант, когда все элементы совпадают

## Особенности
- Получает данные через API plati ([search_api.py](https://github.com/v2rg/platiru-telegram-bot/blob/main/search_api.py))
    - или через парсинг с bs4 ([search_bs4.py](https://github.com/v2rg/platiru-telegram-bot/blob/main/search_bs4.py)) `работает нестабильно`
- Поиск выполняется с помощью разбиения запроса на подстроки
    - результат поиска не всегда идеальный, из-за особенности именования товаров на plati
- Для сортировки ([algo.py](https://github.com/v2rg/platiru-telegram-bot/blob/main/algo.py)) применяются алгоритмы:
    - bubble
    - selection
    - quick
- Кулдаун между запросами — 5 секунд
- Работает на синхронном telebot и получает данные через requests
- *Проект для портфолио и личного использования. На больших нагрузках не тестировался*

## Команды
- `/start` выводит информацию о боте

## Требования
- Python 3.11
- pyTelegramBotAPI
- python-dotenv
- requests
- beautifulsoup4
