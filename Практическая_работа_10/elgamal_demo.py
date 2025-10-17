#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Демонстрация работы алгоритма Эль-Гамаля
Практическая работа №10 - Вариант 7
"""

from elgamal_implementation import ElGamal


def demo_elgamal():
    """Демонстрация работы алгоритма Эль-Гамаля"""
    print("=" * 60)
    print("ДЕМОНСТРАЦИЯ АЛГОРИТМА ЭЛЬ-ГАМАЛЯ")
    print("Практическая работа №10 - Вариант 7")
    print("=" * 60)
    
    elgamal = ElGamal()
    
    # Пример 1: Маленькие числа для демонстрации
    print("\nПРИМЕР 1: Маленькие числа")
    print("-" * 40)
    
    p = 23  # Простое число
    n = 11  # Порядок группы (11 делит 22)
    alpha = 2  # Генератор группы
    
    print(f"Параметры: p={p}, n={n}, alpha={alpha}")
    
    # Проверка параметров
    if elgamal.check_prime(p) and elgamal.check_parameters(p, n, alpha):
        elgamal.p = p
        elgamal.n = n
        elgamal.alpha = alpha
        
        # Генерация ключей
        private_key, public_key = elgamal.generate_keys(p, n, alpha)
        
        # Шифрование
        message = "HELLO"
        print(f"\nШифрование сообщения: '{message}'")
        encrypted = elgamal.encrypt(message, public_key)
        
        # Расшифрование
        decrypted = elgamal.decrypt(encrypted)
        
        print(f"Результат: '{message}' -> '{decrypted}'")
        print(f"Шифрование {'успешно' if message == decrypted else 'неудачно'}")
        
        # Цифровая подпись
        print(f"\nЦифровая подпись для сообщения: '{message}'")
        signature = elgamal.sign(message)
        is_valid = elgamal.verify_signature(message, signature, public_key)
        print(f"Подпись {'валидна' if is_valid else 'невалидна'}")
    
    # Пример 2: Большие числа
    print("\n\nПРИМЕР 2: Большие числа")
    print("-" * 40)
    
    p = 23   # Простое число
    n = 11   # Порядок группы (11 делит 22)
    alpha = 3  # Генератор группы
    
    print(f"Параметры: p={p}, n={n}, alpha={alpha}")
    
    # Проверка параметров
    if elgamal.check_prime(p) and elgamal.check_parameters(p, n, alpha):
        elgamal.p = p
        elgamal.n = n
        elgamal.alpha = alpha
        
        # Генерация ключей
        private_key, public_key = elgamal.generate_keys(p, n, alpha)
        
        # Шифрование
        message = "CRYPTO"
        print(f"\nШифрование сообщения: '{message}'")
        encrypted = elgamal.encrypt(message, public_key)
        
        # Расшифрование
        decrypted = elgamal.decrypt(encrypted)
        
        print(f"Результат: '{message}' -> '{decrypted}'")
        print(f"Шифрование {'успешно' if message == decrypted else 'неудачно'}")
        
        # Цифровая подпись
        print(f"\nЦифровая подпись для сообщения: '{message}'")
        signature = elgamal.sign(message)
        is_valid = elgamal.verify_signature(message, signature, public_key)
        print(f"Подпись {'валидна' if is_valid else 'невалидна'}")
    
    # Пример 3: Персональный вариант (фамилия)
    print("\n\nПРИМЕР 3: Персональный вариант")
    print("-" * 40)
    
    p = 23   # Простое число
    n = 11   # Порядок группы (11 делит 22)
    alpha = 6  # Генератор группы
    
    print(f"Параметры: p={p}, n={n}, alpha={alpha}")
    
    # Проверка параметров
    if elgamal.check_prime(p) and elgamal.check_parameters(p, n, alpha):
        elgamal.p = p
        elgamal.n = n
        elgamal.alpha = alpha
        
        # Генерация ключей
        private_key, public_key = elgamal.generate_keys(p, n, alpha)
        
        # Шифрование персонального сообщения
        message = "STUDENT"  # Замените на свою фамилию
        print(f"\nШифрование персонального сообщения: '{message}'")
        encrypted = elgamal.encrypt(message, public_key)
        
        # Расшифрование
        decrypted = elgamal.decrypt(encrypted)
        
        print(f"Результат: '{message}' -> '{decrypted}'")
        print(f"Шифрование {'успешно' if message == decrypted else 'неудачно'}")
        
        # Цифровая подпись
        print(f"\nЦифровая подпись для персонального сообщения: '{message}'")
        signature = elgamal.sign(message)
        is_valid = elgamal.verify_signature(message, signature, public_key)
        print(f"Подпись {'валидна' if is_valid else 'невалидна'}")


if __name__ == "__main__":
    demo_elgamal()
