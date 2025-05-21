
def get_daily_dua():
    try:
        with open("daily_dua.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    except:
        return "اللهم اغفر لنا وارحمنا واجعلنا من أهل الذكر."
