# Параметры пароля
MIN_PASSWORD_LENGTH = 4
MAX_PASSWORD_LENGTH = 128
DEFAULT_PASSWORD_LENGTH = 12

# Параметры энтропии
ENTROPY_COEFS = {
    "short_passwords": [
        {"max_length": 8, "factor": 0.4},
        {"max_length": 12, "factor": 0.75},
    ],
    "unique_ratio": 1.5,
    "ascii_sequence": 0.6,
    "keyboard_sequence": 0.5,
    "digits_only": 0.3,
    "dictionary": 0.05,
}
