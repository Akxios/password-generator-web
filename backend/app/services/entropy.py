import math
import string
from collections import Counter

from backend.app.services.config import KEYBOARD_SEQS, COMMON_PASSWORDS
from backend.config import ENTROPY_COEFS


def ascii_sequence_len(password: str) -> int:
    max_len = curr = 1

    for i in range(1, len(password)):
        diff = ord(password[i]) - ord(password[i - 1])
        if diff in (1, -1):
            curr += 1
            max_len = max(max_len, curr)
        else:
            curr = 1

    return max_len


def keyboard_sequence_len(password: str) -> int:
    p = password.lower()
    max_len = 1

    for seq in KEYBOARD_SEQS:
        for s in (seq, seq[::-1]):
            for i in range(len(s)):
                for j in range(i + 3, len(s) + 1):
                    if s[i:j] in p:
                        max_len = max(max_len, j - i)

    return max_len


def repeated_substring_ratio(password: str) -> float:
    """
    Возвращает долю повторяющихся паттернов
    abcabc -> ~0.5
    """
    length = len(password)
    for size in range(1, length // 2 + 1):
        chunk = password[:size]
        if chunk * (length // size) == password:
            return 1 - (size / length)
    return 0.0


def shannon_entropy(password: str) -> float:
    length = len(password)
    freq = Counter(password)

    H = 0.0
    for count in freq.values():
        p = count / length
        H -= p * math.log2(p)

    return H * length


def alphabet_size(password: str) -> int:
    size = 0
    if any(c.islower() for c in password):
        size += 26
    if any(c.isupper() for c in password):
        size += 26
    if any(c.isdigit() for c in password):
        size += 10
    if any(c in string.punctuation for c in password):
        size += len(string.punctuation)
    return size


def password_strength_report(password: str) -> float:
    """Возвращает подробный отчёт о пароле с энтропией и паттернами"""
    length = len(password)

    if length == 0:
        return {"entropy": 0.0}

    # Базовая энтропия
    alpha = alphabet_size(password)
    brute_entropy = math.log2(alpha) * length
    real_entropy = shannon_entropy(password)
    entropy = min(brute_entropy, real_entropy)

    # Короткие пароли
    for rule in ENTROPY_COEFS["short_passwords"]:
        if length <= rule["max_length"]:
            entropy *= rule["factor"]
            break  # применяем только первый подходящий диапазон

    # Повторы
    unique_ratio = len(set(password)) / length
    entropy *= unique_ratio ** ENTROPY_COEFS["unique_ratio"]

    # Повторяющиеся паттерны
    rep_ratio = repeated_substring_ratio(password)
    entropy *= (1 - rep_ratio)

    # ASCII последовательности
    ascii_len = ascii_sequence_len(password)
    if ascii_len >= 3:
        entropy *= ENTROPY_COEFS["ascii_sequence"] ** (ascii_len - 2)

    # Клавиатурные последовательности
    key_len = keyboard_sequence_len(password)
    if key_len >= 3:
        entropy *= ENTROPY_COEFS["keyboard_sequence"] ** (key_len - 2)

    # Чисто цифры
    is_digits_only = password.isdigit()
    if is_digits_only:
        entropy *= ENTROPY_COEFS["digits_only"]

    # Словарь
    in_dictionary = password.lower() in COMMON_PASSWORDS
    if in_dictionary:
        entropy *= ENTROPY_COEFS["dictionary"]

    entropy = round(max(entropy, 0.0), 2)

    return {
        "entropy": entropy,
        "length": length,
        "unique_ratio": round(unique_ratio, 2),
        "repeat_ratio": round(rep_ratio, 2),
        "ascii_sequence": ascii_len,
        "keyboard_sequence": key_len,
        "digits_only": is_digits_only,
        "in_dictionary": in_dictionary
    }
