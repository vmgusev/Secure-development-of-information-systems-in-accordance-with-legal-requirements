#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Реализация алгоритма RSA для шифрования и расшифрования текстовых сообщений
Практическая работа №9 - Вариант 7

Автор: Гусев В.М. КВМО-11-24
Дата: 2025

Требования:
1.1 Простые числа p и q задаются пользователем
1.2 Проверка простоты чисел различными методами
1.3 Число e вводится пользователем или подбирается программой
1.4 Число d вычисляется алгоритмом Евклида
1.5 Шифрование собственной фамилии
1.6 Обратимое преобразование текста в числа
1.7 Эксперимент с закрытым ключом
1.8 Эксперимент с открытым ключом
1.9 Все функции реализованы самостоятельно
"""

import math
import random
from typing import Tuple, List, Optional


class RSAImplementation:
    """
    Класс для реализации алгоритма RSA
    """
    
    def __init__(self):
        """Инициализация RSA"""
        self.p = 0
        self.q = 0
        self.n = 0
        self.phi = 0
        self.e = 0
        self.d = 0
        self.public_key = (0, 0)
        self.private_key = (0, 0)
    
    def is_prime_simple(self, n: int) -> bool:
        """
        Простая проверка простоты числа методом перебора
        Проверяет деление на все числа от 2 до √n
        """
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        
        # Проверяем только нечетные делители до √n
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        return True
    
    def is_prime_fermat(self, n: int, k: int = 10) -> bool:
        """
        Проверка простоты числа с помощью малой теоремы Ферма
        Если n простое, то a^(n-1) ≡ 1 (mod n) для всех a, взаимно простых с n
        """
        if n < 2:
            return False
        if n == 2 or n == 3:
            return True
        if n % 2 == 0:
            return False
        
        # Проверяем k случайных оснований
        for _ in range(k):
            a = random.randint(2, n - 2)
            if self.gcd(a, n) != 1:
                return False
            if self.modular_exponentiation(a, n - 1, n) != 1:
                return False
        return True
    
    def is_prime_miller_rabin(self, n: int, k: int = 10) -> bool:
        """
        Проверка простоты числа с помощью теста Миллера-Рабина
        """
        if n < 2:
            return False
        if n == 2 or n == 3:
            return True
        if n % 2 == 0:
            return False
        
        # Записываем n-1 в виде d * 2^r
        r = 0
        d = n - 1
        while d % 2 == 0:
            r += 1
            d //= 2
        
        # Проводим k раундов теста
        for _ in range(k):
            a = random.randint(2, n - 2)
            x = self.modular_exponentiation(a, d, n)
            
            if x == 1 or x == n - 1:
                continue
            
            for _ in range(r - 1):
                x = (x * x) % n
                if x == n - 1:
                    break
            else:
                return False
        return True
    
    def gcd(self, a: int, b: int) -> int:
        """
        Нахождение наибольшего общего делителя алгоритмом Евклида
        """
        while b:
            a, b = b, a % b
        return a
    
    def extended_gcd(self, a: int, b: int) -> Tuple[int, int, int]:
        """
        Расширенный алгоритм Евклида
        Возвращает (gcd, x, y) такие, что ax + by = gcd(a, b)
        """
        if a == 0:
            return b, 0, 1
        
        gcd, x1, y1 = self.extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    def modular_inverse(self, a: int, m: int) -> Optional[int]:
        """
        Нахождение обратного элемента по модулю с помощью расширенного алгоритма Евклида
        """
        gcd, x, y = self.extended_gcd(a, m)
        if gcd != 1:
            return None  # Обратный элемент не существует
        return (x % m + m) % m
    
    def modular_exponentiation(self, base: int, exponent: int, modulus: int) -> int:
        """
        Быстрое возведение в степень по модулю
        """
        result = 1
        base = base % modulus
        
        while exponent > 0:
            if exponent % 2 == 1:
                result = (result * base) % modulus
            exponent = exponent >> 1
            base = (base * base) % modulus
        
        return result
    
    def check_prime(self, n: int) -> dict:
        """
        Комплексная проверка простоты числа всеми методами
        """
        results = {
            'number': n,
            'simple_test': self.is_prime_simple(n),
            'fermat_test': self.is_prime_fermat(n),
            'miller_rabin_test': self.is_prime_miller_rabin(n),
            'is_prime': False
        }
        
        # Число считается простым, если все тесты дали положительный результат
        results['is_prime'] = (results['simple_test'] and 
                              results['fermat_test'] and 
                              results['miller_rabin_test'])
        
        return results
    
    def find_e(self, phi: int, user_e: Optional[int] = None) -> int:
        """
        Поиск числа e (открытой экспоненты)
        Если пользователь не указал e, подбираем автоматически
        """
        if user_e is not None:
            # Проверяем пользовательское значение e
            if self.gcd(user_e, phi) == 1 and 1 < user_e < phi:
                return user_e
            else:
                print(f"Ошибка: e = {user_e} не подходит. НОД(e, φ) = {self.gcd(user_e, phi)}")
                print("Подбираем e автоматически...")
        
        # Подбираем e автоматически
        # Начинаем с небольших простых чисел
        candidates = [3, 5, 17, 257, 65537]
        
        for candidate in candidates:
            if self.gcd(candidate, phi) == 1 and 1 < candidate < phi:
                return candidate
        
        # Если стандартные значения не подошли, ищем случайно
        for _ in range(1000):
            candidate = random.randint(2, phi - 1)
            if self.gcd(candidate, phi) == 1:
                return candidate
        
        raise ValueError("Не удалось найти подходящее значение e")
    
    def generate_keys(self, p: int, q: int, user_e: Optional[int] = None) -> bool:
        """
        Генерация ключей RSA
        """
        print("Генерация ключей RSA...")
        print("=" * 50)
        
        # Проверяем простоту p и q
        print(f"Проверка простоты числа p = {p}:")
        p_check = self.check_prime(p)
        self.print_prime_check(p_check)
        
        print(f"\nПроверка простоты числа q = {q}:")
        q_check = self.check_prime(q)
        self.print_prime_check(q_check)
        
        if not p_check['is_prime'] or not q_check['is_prime']:
            print("\nОшибка: p и q должны быть простыми числами!")
            return False
        
        # Сохраняем p и q
        self.p = p
        self.q = q
        
        # Вычисляем n = p * q
        self.n = p * q
        print(f"\nn = p * q = {p} * {q} = {self.n}")
        
        # Вычисляем φ(n) = (p-1)(q-1)
        self.phi = (p - 1) * (q - 1)
        print(f"φ(n) = (p-1)(q-1) = ({p}-1)({q}-1) = {self.phi}")
        
        # Находим e
        self.e = self.find_e(self.phi, user_e)
        print(f"e = {self.e}")
        
        # Вычисляем d (закрытую экспоненту)
        self.d = self.modular_inverse(self.e, self.phi)
        if self.d is None:
            print("Ошибка: не удалось найти обратный элемент для e")
            return False
        
        print(f"d = e^(-1) mod φ(n) = {self.d}")
        
        # Формируем ключи
        self.public_key = (self.e, self.n)
        self.private_key = (self.d, self.n)
        
        print(f"\nОткрытый ключ: (e, n) = ({self.e}, {self.n})")
        print(f"Закрытый ключ: (d, n) = ({self.d}, {self.n})")
        
        return True
    
    def print_prime_check(self, check_result: dict):
        """Вывод результатов проверки простоты"""
        print(f"  Простой тест: {'✓' if check_result['simple_test'] else '✗'}")
        print(f"  Тест Ферма: {'✓' if check_result['fermat_test'] else '✗'}")
        print(f"  Тест Миллера-Рабина: {'✓' if check_result['miller_rabin_test'] else '✗'}")
        print(f"  Итоговый результат: {'Простое' if check_result['is_prime'] else 'Составное'}")
    
    def text_to_numbers(self, text: str) -> List[int]:
        """
        Преобразование текста в числа
        Алгоритм: каждый символ кодируется как (ASCII код + 1000)
        Это обеспечивает обратимость и избегает проблем с нулями
        """
        numbers = []
        for char in text:
            ascii_code = ord(char)
            encoded = ascii_code + 1000  # Добавляем 1000 для избежания нулей
            numbers.append(encoded)
        return numbers
    
    def numbers_to_text(self, numbers: List[int]) -> str:
        """
        Преобразование чисел обратно в текст
        """
        text = ""
        for num in numbers:
            ascii_code = num - 1000  # Вычитаем 1000
            text += chr(ascii_code)
        return text
    
    def encrypt(self, message: str, key: Tuple[int, int]) -> List[int]:
        """
        Шифрование сообщения
        """
        print(f"Шифрование сообщения: '{message}'")
        print(f"Используемый ключ: {key}")
        
        # Преобразуем текст в числа
        numbers = self.text_to_numbers(message)
        print(f"Текст в числах: {numbers}")
        
        # Шифруем каждое число
        encrypted = []
        exponent, modulus = key
        
        for num in numbers:
            if num >= modulus:
                print(f"Предупреждение: число {num} >= модуля {modulus}")
                # Разбиваем большое число на части
                parts = self.encrypt_large_number(num, key)
                # Добавляем маркер, что это большое число
                encrypted.append(modulus)  # Маркер начала большого числа
                encrypted.extend(parts)
                encrypted.append(modulus + 1)  # Маркер конца большого числа
            else:
                encrypted_num = self.modular_exponentiation(num, exponent, modulus)
                encrypted.append(encrypted_num)
        
        print(f"Зашифрованные числа: {encrypted}")
        return encrypted
    
    def encrypt_large_number(self, num: int, key: Tuple[int, int]) -> List[int]:
        """
        Шифрование большого числа (больше модуля)
        Разбиваем число на части
        """
        exponent, modulus = key
        parts = []
        
        # Разбиваем число на части, каждая меньше модуля
        while num > 0:
            part = num % modulus
            parts.append(part)
            num //= modulus
        
        # Шифруем каждую часть
        encrypted_parts = []
        for part in parts:
            encrypted_part = self.modular_exponentiation(part, exponent, modulus)
            encrypted_parts.append(encrypted_part)
        
        return encrypted_parts
    
    def decrypt_large_number(self, encrypted_parts: List[int], key: Tuple[int, int]) -> int:
        """
        Расшифрование большого числа из частей
        """
        exponent, modulus = key
        decrypted_parts = []
        
        # Расшифровываем каждую часть
        for encrypted_part in encrypted_parts:
            decrypted_part = self.modular_exponentiation(encrypted_part, exponent, modulus)
            decrypted_parts.append(decrypted_part)
        
        # Собираем число из частей
        result = 0
        multiplier = 1
        for part in decrypted_parts:
            result += part * multiplier
            multiplier *= modulus
        
        return result
    
    def decrypt(self, encrypted_numbers: List[int], key: Tuple[int, int]) -> str:
        """
        Расшифрование сообщения
        """
        print(f"Расшифрование чисел: {encrypted_numbers}")
        print(f"Используемый ключ: {key}")
        
        # Расшифровываем каждое число
        decrypted_numbers = []
        exponent, modulus = key
        
        i = 0
        while i < len(encrypted_numbers):
            if encrypted_numbers[i] == modulus:
                # Маркер начала большого числа
                i += 1
                parts = []
                # Собираем части большого числа
                while i < len(encrypted_numbers) and encrypted_numbers[i] != modulus + 1:
                    parts.append(encrypted_numbers[i])
                    i += 1
                # Пропускаем маркер конца
                i += 1
                
                # Расшифровываем большое число
                decrypted_large = self.decrypt_large_number(parts, key)
                decrypted_numbers.append(decrypted_large)
            else:
                # Обычное число
                decrypted_num = self.modular_exponentiation(encrypted_numbers[i], exponent, modulus)
                decrypted_numbers.append(decrypted_num)
                i += 1
        
        print(f"Расшифрованные числа: {decrypted_numbers}")
        
        # Преобразуем числа обратно в текст
        message = self.numbers_to_text(decrypted_numbers)
        print(f"Расшифрованное сообщение: '{message}'")
        
        return message
    
    def demonstrate_rsa(self, message: str, user_p: int, user_q: int, user_e: Optional[int] = None):
        """
        Демонстрация работы RSA
        """
        print("ДЕМОНСТРАЦИЯ АЛГОРИТМА RSA")
        print("=" * 60)
        
        # Генерируем ключи
        if not self.generate_keys(user_p, user_q, user_e):
            return
        
        print("\n" + "=" * 60)
        print("ЭКСПЕРИМЕНТ 1: Шифрование открытым ключом, расшифрование закрытым")
        print("=" * 60)
        
        # Шифруем открытым ключом
        encrypted = self.encrypt(message, self.public_key)
        
        # Расшифровываем закрытым ключом
        decrypted = self.decrypt(encrypted, self.private_key)
        
        print(f"\nРезультат: {message == decrypted}")
        if message == decrypted:
            print("✓ Эксперимент 1 прошел успешно!")
        else:
            print("✗ Эксперимент 1 не удался!")
        
        print("\n" + "=" * 60)
        print("ЭКСПЕРИМЕНТ 2: Шифрование закрытым ключом, расшифрование открытым")
        print("=" * 60)
        
        # Шифруем закрытым ключом
        encrypted_private = self.encrypt(message, self.private_key)
        
        # Расшифровываем открытым ключом
        decrypted_public = self.decrypt(encrypted_private, self.public_key)
        
        print(f"\nРезультат: {message == decrypted_public}")
        if message == decrypted_public:
            print("✓ Эксперимент 2 прошел успешно!")
        else:
            print("✗ Эксперимент 2 не удался!")
        
        print("\n" + "=" * 60)
        print("ЭКСПЕРИМЕНТ 3: Попытка расшифровать открытым ключом то, что зашифровано открытым ключом")
        print("=" * 60)
        
        # Шифруем открытым ключом
        encrypted_public = self.encrypt(message, self.public_key)
        
        # Пытаемся расшифровать тем же открытым ключом
        try:
            decrypted_same = self.decrypt(encrypted_public, self.public_key)
            print(f"Результат расшифровки тем же ключом: '{decrypted_same}'")
            print(f"Совпадает с исходным: {message == decrypted_same}")
            if message != decrypted_same:
                print("✓ Эксперимент 3 прошел успешно! (как и ожидалось)")
            else:
                print("✗ Эксперимент 3 не удался! (неожиданно)")
        except Exception as e:
            print(f"Ошибка при попытке расшифровки: {e}")
            print("✓ Эксперимент 3 прошел успешно! (как и ожидалось)")


def main():
    """Основная функция программы"""
    print("РЕАЛИЗАЦИЯ АЛГОРИТМА RSA")
    print("Практическая работа №9 - Вариант 7")
    print("=" * 60)
    
    # Создаем экземпляр RSA
    rsa = RSAImplementation()
    
    # Сообщение для шифрования (фамилия)
    message = "Иванов"  # Замените на свою фамилию
    
    print(f"Сообщение для шифрования: '{message}'")
    print()
    
    # Запрашиваем у пользователя простые числа
    print("Введите простые числа p и q:")
    try:
        p = int(input("p = "))
        q = int(input("q = "))
        
        # Спрашиваем про e
        e_input = input("Введите e (или нажмите Enter для автоматического подбора): ")
        user_e = int(e_input) if e_input.strip() else None
        
        # Демонстрируем работу RSA
        rsa.demonstrate_rsa(message, p, q, user_e)
        
    except ValueError as e:
        print(f"Ошибка ввода: {e}")
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")


if __name__ == "__main__":
    main()
