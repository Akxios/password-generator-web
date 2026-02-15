from zxcvbn import zxcvbn


def password_strength_report(password: str) -> dict:
    if not password:
        # Возвращаем "заглушки" для пустой строки
        empty_times = {
            "online_throttling_100_per_hour": "instantly",
            "online_no_throttling_10_per_second": "instantly",
            "offline_slow_hashing_1e4_per_second": "instantly",
            "offline_fast_hashing_1e10_per_second": "instantly",
        }
        return {
            "score": 0,
            "crack_times_display": empty_times,
            "guesses": 0,
            "warning": None,
            "suggestions": [],
        }

    results = zxcvbn(password)

    return {
        "score": results["score"],
        # zxcvbn уже возвращает нужную структуру в этом поле
        "crack_times_display": results["crack_times_display"],
        "guesses": results["guesses"],
        "warning": results["feedback"]["warning"] or None,
        "suggestions": results["feedback"]["suggestions"],
    }
