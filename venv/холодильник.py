from datetime import datetime, timedelta
from decimal import Decimal

DATE_FORMAT = '%Y-%m-%d'


def add(items, title, amount, expiration_date=None):
    if title not in items:
        items[title] = []
    if expiration_date:
        expiration_date = datetime.strptime(expiration_date, DATE_FORMAT).date()
    items[title].append({'amount': Decimal(amount), 'expiration_date': expiration_date})


def add_by_note(items, note):
    parts = note.split()
    if len(parts) > 1 and len(parts[-1].split('-')) == 3:
        expiration_date = parts[-1]
        good_amount = Decimal(parts[-2])
        title = " ".join(parts[:-2])
    else:
        expiration_date = None
        good_amount = Decimal(parts[-1])
        title = " ".join(parts[:-1])

    add(items, title, good_amount, expiration_date)


def find(items, needle):
    results = []
    for title in items:
        if needle.lower() in title.lower():
            results.append(title)
    return results


def amount(items, needle):
    total_amount = Decimal(0)
    found_items = find(items, needle)
    for title in found_items:
        for batch in items[title]:
            total_amount += batch['amount']
    return total_amount


def expire(items, in_advance_days=0):
    today = datetime.today().date()  # Текущая дата
    expire_date = today + timedelta(days=in_advance_days)  # Дата истечения

    expiring_soon = []
    for title, batches in items.items():
        for batch in batches:
            # Проверяем, если срок годности указан и если товар истекает
            if batch['expiration_date'] is not None and batch['expiration_date'] <= expire_date:
                expiring_soon.append({
                    'title': title,
                    'expiration_date': batch['expiration_date'],
                    'amount': batch['amount']
                })

    return expiring_soon


# Пример использования
goods = {}
add(goods, 'Макароны', 1.5)
add(goods, 'Яйца', 4, '2023-07-15')
add(goods, 'Молоко', 5, '2024-11-20')
add(goods, 'Хлеб', 2)  # Без срока годности
add_by_note(goods, 'Хлеб 3 2025-03-01')