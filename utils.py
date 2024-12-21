import logging
from functools import wraps

# Декоратор для обробки помилок
def error_handler(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error occurred: {e}")
            # Можна додати відповідь користувачу, що сталася помилка
    return wrapper
