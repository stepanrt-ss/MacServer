from datetime import date, timedelta


start_date = date(2025, 1, 15)

days_left = (start_date + timedelta(days=30) - date.today()).days
if days_left > 0:
    print(f"До конца подписки осталось {days_left} дней")
else:
    print("Подписка уже истекла")




