#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Демонстрационная программа для алгоритма RSA
Практическая работа №9 - Вариант 7

Автор: Гусев В.М. КВМО-11-24
Дата: 2025

Демонстрирует различные аспекты работы RSA:
- Проверку простоты чисел
- Генерацию ключей
- Шифрование и расшифрование
- Различные эксперименты
"""

from rsa_implementation import RSAImplementation


def demo_prime_tests():
    """Демонстрация различных тестов простоты"""
    print("ДЕМОНСТРАЦИЯ ТЕСТОВ ПРОСТОТЫ")
    print("=" * 50)
    
    rsa = RSAImplementation()
    
    # Тестируем различные числа
    test_numbers = [17, 19, 25, 29, 31, 35, 37, 41, 49, 53, 97, 101, 121, 127]
    
    for num in test_numbers:
        print(f"\nТестируем число {num}:")
        result = rsa.check_prime(num)
        rsa.print_prime_check(result)
    
    print("\n" + "=" * 50)


def demo_key_generation():
    """Демонстрация генерации ключей"""
    print("ДЕМОНСТРАЦИЯ ГЕНЕРАЦИИ КЛЮЧЕЙ")
    print("=" * 50)
    
    rsa = RSAImplementation()
    
    # Пример 1: Маленькие простые числа
    print("Пример 1: p=11, q=13")
    rsa.generate_keys(11, 13)
    
    print("\n" + "-" * 30)
    
    # Пример 2: Средние простые числа
    print("Пример 2: p=17, q=19")
    rsa.generate_keys(17, 19)
    
    print("\n" + "=" * 50)


def demo_text_conversion():
    """Демонстрация преобразования текста в числа и обратно"""
    print("ДЕМОНСТРАЦИЯ ПРЕОБРАЗОВАНИЯ ТЕКСТА")
    print("=" * 50)
    
    rsa = RSAImplementation()
    
    test_messages = ["Hello", "RSA", "Криптография", "123", "АБВ"]
    
    for message in test_messages:
        print(f"\nИсходное сообщение: '{message}'")
        
        # Преобразуем в числа
        numbers = rsa.text_to_numbers(message)
        print(f"В числах: {numbers}")
        
        # Преобразуем обратно в текст
        restored = rsa.numbers_to_text(numbers)
        print(f"Восстановлено: '{restored}'")
        print(f"Совпадает: {message == restored}")
    
    print("\n" + "=" * 50)


def demo_encryption_decryption():
    """Демонстрация шифрования и расшифрования"""
    print("ДЕМОНСТРАЦИЯ ШИФРОВАНИЯ И РАСШИФРОВАНИЯ")
    print("=" * 50)
    
    rsa = RSAImplementation()
    
    # Генерируем ключи
    print("Генерируем ключи для p=11, q=13...")
    rsa.generate_keys(11, 13)
    
    # Тестируем различные сообщения
    test_messages = ["Hi", "RSA", "Test", "123", "A"]
    
    for message in test_messages:
        print(f"\nТестируем сообщение: '{message}'")
        
        # Шифруем открытым ключом
        encrypted = rsa.encrypt(message, rsa.public_key)
        
        # Расшифровываем закрытым ключом
        decrypted = rsa.decrypt(encrypted, rsa.private_key)
        
        print(f"Результат: {message == decrypted}")
    
    print("\n" + "=" * 50)


def demo_large_numbers():
    """Демонстрация работы с большими числами"""
    print("ДЕМОНСТРАЦИЯ РАБОТЫ С БОЛЬШИМИ ЧИСЛАМИ")
    print("=" * 50)
    
    rsa = RSAImplementation()
    
    # Используем большие простые числа
    print("Используем p=101, q=103 (n=10403)")
    rsa.generate_keys(101, 103)
    
    # Тестируем сообщение, которое может дать большое число
    message = "Hello World!"
    print(f"\nТестируем сообщение: '{message}'")
    
    # Преобразуем в числа
    numbers = rsa.text_to_numbers(message)
    print(f"Числа: {numbers}")
    
    # Проверяем, какие числа больше модуля
    for i, num in enumerate(numbers):
        if num >= rsa.n:
            print(f"Число {num} (символ '{message[i]}') больше модуля {rsa.n}")
    
    # Шифруем и расшифровываем
    encrypted = rsa.encrypt(message, rsa.public_key)
    decrypted = rsa.decrypt(encrypted, rsa.private_key)
    
    print(f"Результат: {message == decrypted}")
    
    print("\n" + "=" * 50)


def demo_error_cases():
    """Демонстрация обработки ошибок"""
    print("ДЕМОНСТРАЦИЯ ОБРАБОТКИ ОШИБОК")
    print("=" * 50)
    
    rsa = RSAImplementation()
    
    # Тест 1: Составные числа
    print("Тест 1: Попытка использовать составные числа")
    try:
        rsa.generate_keys(15, 21)  # 15 = 3*5, 21 = 3*7
    except Exception as e:
        print(f"Ошибка: {e}")
    
    print("\n" + "-" * 30)
    
    # Тест 2: Неподходящее значение e
    print("Тест 2: Неподходящее значение e")
    try:
        rsa.generate_keys(11, 13, 12)  # 12 не взаимно просто с φ(143)=120
    except Exception as e:
        print(f"Ошибка: {e}")
    
    print("\n" + "-" * 30)
    
    # Тест 3: Одинаковые простые числа
    print("Тест 3: Одинаковые простые числа")
    try:
        rsa.generate_keys(11, 11)
    except Exception as e:
        print(f"Ошибка: {e}")
    
    print("\n" + "=" * 50)


def interactive_demo():
    """Интерактивная демонстрация"""
    print("ИНТЕРАКТИВНАЯ ДЕМОНСТРАЦИЯ")
    print("=" * 50)
    
    rsa = RSAImplementation()
    
    while True:
        print("\nВыберите действие:")
        print("1. Проверить простоту числа")
        print("2. Сгенерировать ключи")
        print("3. Зашифровать сообщение")
        print("4. Расшифровать сообщение")
        print("5. Полная демонстрация")
        print("0. Выход")
        
        choice = input("\nВаш выбор: ").strip()
        
        if choice == "0":
            break
        elif choice == "1":
            try:
                num = int(input("Введите число для проверки: "))
                result = rsa.check_prime(num)
                rsa.print_prime_check(result)
            except ValueError:
                print("Ошибка: введите целое число")
        
        elif choice == "2":
            try:
                p = int(input("Введите p: "))
                q = int(input("Введите q: "))
                e_input = input("Введите e (или Enter для автоподбора): ")
                user_e = int(e_input) if e_input.strip() else None
                rsa.generate_keys(p, q, user_e)
            except ValueError:
                print("Ошибка: введите целые числа")
        
        elif choice == "3":
            if rsa.n == 0:
                print("Сначала сгенерируйте ключи!")
                continue
            message = input("Введите сообщение для шифрования: ")
            key_choice = input("Использовать открытый (1) или закрытый (2) ключ? ")
            key = rsa.public_key if key_choice == "1" else rsa.private_key
            rsa.encrypt(message, key)
        
        elif choice == "4":
            if rsa.n == 0:
                print("Сначала сгенерируйте ключи!")
                continue
            try:
                encrypted_str = input("Введите зашифрованные числа через пробел: ")
                encrypted = [int(x) for x in encrypted_str.split()]
                key_choice = input("Использовать открытый (1) или закрытый (2) ключ? ")
                key = rsa.public_key if key_choice == "1" else rsa.private_key
                rsa.decrypt(encrypted, key)
            except ValueError:
                print("Ошибка: введите числа через пробел")
        
        elif choice == "5":
            try:
                message = input("Введите сообщение для демонстрации: ")
                p = int(input("Введите p: "))
                q = int(input("Введите q: "))
                e_input = input("Введите e (или Enter для автоподбора): ")
                user_e = int(e_input) if e_input.strip() else None
                rsa.demonstrate_rsa(message, p, q, user_e)
            except ValueError:
                print("Ошибка: введите целые числа")
        
        else:
            print("Неверный выбор!")


def main():
    """Основная функция демонстрации"""
    print("ДЕМОНСТРАЦИОННАЯ ПРОГРАММА RSA")
    print("Практическая работа №9 - Вариант 7")
    print("=" * 60)
    
    while True:
        print("\nВыберите демонстрацию:")
        print("1. Тесты простоты")
        print("2. Генерация ключей")
        print("3. Преобразование текста")
        print("4. Шифрование/расшифрование")
        print("5. Большие числа")
        print("6. Обработка ошибок")
        print("7. Интерактивная демонстрация")
        print("0. Выход")
        
        choice = input("\nВаш выбор: ").strip()
        
        if choice == "0":
            break
        elif choice == "1":
            demo_prime_tests()
        elif choice == "2":
            demo_key_generation()
        elif choice == "3":
            demo_text_conversion()
        elif choice == "4":
            demo_encryption_decryption()
        elif choice == "5":
            demo_large_numbers()
        elif choice == "6":
            demo_error_cases()
        elif choice == "7":
            interactive_demo()
        else:
            print("Неверный выбор!")
        
        input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    main()
