import secrets
import string


def generate_cryptographic_password(
    length: int = 12,
    use_lower: bool = True,
    use_upper: bool = True,
    use_digits: bool = True,
    use_special: bool = True
) -> str:
    """
    Генерирует криптографически стойкий пароль.

    Гарантирует наличие как минимум одного символа
    из каждого выбранного класса.
    """
    pools = []

    if use_lower:
        pools.append(string.ascii_lowercase)
    if use_upper:
        pools.append(string.ascii_uppercase)
    if use_digits:
        pools.append(string.digits)
    if use_special:
        pools.append(string.punctuation)

    if not pools:
        raise ValueError("Нужно выбрать хотя бы один тип символов")

    if length < len(pools):
        raise ValueError("Длина пароля меньше количества выбранных типов символов")

    password = [secrets.choice(pool) for pool in pools]
    all_chars = ''.join(pools)

    password += [secrets.choice(all_chars) for _ in range(length - len(password))]

    secrets.SystemRandom().shuffle(password)

    return ''.join(password)
