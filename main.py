import datetime as dt


class Record:
    def __init__(self, amount, comment, date=''): 
        # Пустые дефолтные значения лучше указывать как None и сравнивать с помощью оператора 'is'.
        # Дело в том, что стандартный интерпретатор питона - CPython - имеет встроенные объекты, которые создаются при запуске интерпретатора.
        # Среди них None - объект типа NoneType. Его, в частности, возвращают функции при отсутствии return.
        # Оператор is сравнивает внутренний id объектов в Питоне. Соответсвтенно, если мы зададим дефолтное значение аргумента в функции None,
        # то во-первых - питон не будет создавать объект пустой строки при инициализации функции, во-вторых - при использовании is мы не сравниваем два объекта,
        # а сравниваем два целочисленных числа, что довольно простая операция для компьютера.
        # Микрооптимизация, но тем не менее оптимизация
        self.amount = amount
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date()) 
        # Здесь более лаконично смотрелось бы разбиение на логические шаги -
        # (
        #     dt.datetime.now().date()
        #     if date is None
        #     else dt.dtatetime.strptime(date, '%d.%m.%Y')
        # )
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        for Record in self.records:
            if Record.date == dt.datetime.now().date():
                # Более лаконично 
                # today_stats += Record.amount
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        # А почему бы нам не использовать здесь list comprehension? Он же прекрасен! И в нем можно проверять условия!
        for record in self.records:
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        # Комментарии хороши там, где без них не разобраться. Здесь же название функции исчерпывающее
        x = self.limit - self.get_today_stats()
        if x > 0:
            # Напоминаю, что слеши для переноса строк мы не используем. Выше по коду в Record есть прекрасные пример, как нужно. Скобочки наше все!
            # И в первой строке можно не использовать f-string, излишне
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            return('Хватит есть!')


class CashCalculator(Calculator):
    # Тут, кстати, комментарии не излишне, так как если будет какая-нибудь экзотичная валюта, ее аббревиатуру не всегда можно сразу понять. 
    # А комментарий можно найти в поиске по коду
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE): # Константы доступны внутри класса через self.*_RATE Инициализировать их в аргументах излишне
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            cash_remained == 1.00 # Очепятка! Тут же деление нужно, а не сравнение
            currency_type = 'руб'
        # Я бы добавил тут else и выводил бы ошибку, что валюта не распознана. Но ты действуй на свой страх и риск ;)
        
        if cash_remained > 0:
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            # Скобочки, нельзя слэш. Вот так тут ставится запятая и никак иначе. Как в примере выше
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)
            # Тут сразу два момента касающегося очень важной проблемы - однообразия
            # 1 - по всюду в коде были использованы f-string (и правильно! они быстрее и красивее), а здесь почему то .format(). Неконсистентно!
            # 2 - До этого в коде для форматирования float в строку использоавалась встроенная функция round(), а здесь :.2f. Нужно выбрать что то одно 


    # Излишне добавленный метод, ведь здесь мы не переопределяем никакую логику, а лишь вызываем метод класса родителя! 
    # А он доступен нам и без декларации оного!
    def get_week_stats(self):
        super().get_week_stats()
