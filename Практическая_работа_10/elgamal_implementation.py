#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Реализация алгоритма Эль-Гамаля
Практическая работа №10 - Вариант 7
"""

import random
import math
from typing import Tuple, List


class ElGamal:
    """Класс для реализации алгоритма Эль-Гамаля"""
    
    def __init__(self):
        self.p = 0  # Простое число
        self.n = 0  # Порядок группы
        self.alpha = 0  # Генератор группы
        self.private_key = 0  # Закрытый ключ
        self.public_key = 0  # Открытый ключ
    
    def is_prime(self, n: int) -> bool:
        """Проверка числа на простоту методом перебора"""
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        return True
    
    def miller_rabin_test(self, n: int, k: int = 10) -> bool:
        """Тест Миллера-Рабина для проверки простоты"""
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
            a = random.randrange(2, n - 1)
            x = pow(a, d, n)
            
            if x == 1 or x == n - 1:
                continue
            
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        
        return True
    
    def fermat_test(self, n: int, k: int = 10) -> bool:
        """Малая теорема Ферма для проверки простоты"""
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        
        for _ in range(k):
            a = random.randrange(2, n)
            if pow(a, n - 1, n) != 1:
                return False
        return True
    
    def check_prime(self, p: int) -> bool:
        """Комплексная проверка простоты числа"""
        print(f"Проверка простоты числа {p}...")
        
        # Сначала быстрая проверка перебором
        if not self.is_prime(p):
            print("❌ Число не является простым (проверка перебором)")
            return False
        
        # Затем тест Миллера-Рабина для больших чисел
        if p > 1000:
            if not self.miller_rabin_test(p):
                print("❌ Число не является простым (тест Миллера-Рабина)")
                return False
        
        # Дополнительная проверка тестом Ферма
        if not self.fermat_test(p):
            print("❌ Число не является простым (тест Ферма)")
            return False
        
        print("✅ Число является простым")
        return True
    
    def check_parameters(self, p: int, n: int, alpha: int) -> bool:
        """Проверка допустимости параметров n и alpha"""
        print(f"Проверка параметров n={n}, alpha={alpha} для p={p}...")
        
        # Проверяем, что n делит p-1
        if (p - 1) % n != 0:
            print(f"❌ n={n} не делит p-1={p-1}")
            return False
        
        # Проверяем, что alpha^n ≡ 1 (mod p)
        if pow(alpha, n, p) != 1:
            print(f"❌ alpha^{n} ≢ 1 (mod {p})")
            return False
        
        # Проверяем, что alpha не является корнем меньшей степени
        for i in range(1, n):
            if pow(alpha, i, p) == 1:
                print(f"❌ alpha^{i} ≡ 1 (mod {p}), но i={i} < n={n}")
                return False
        
        print("✅ Параметры корректны")
        return True
    
    def generate_keys(self, p: int, n: int, alpha: int) -> Tuple[int, int]:
        """Генерация ключевой пары"""
        print("Генерация ключевой пары...")
        
        # Генерируем закрытый ключ
        self.private_key = random.randrange(1, n)
        
        # Вычисляем открытый ключ
        self.public_key = pow(alpha, self.private_key, p)
        
        print(f"Закрытый ключ: {self.private_key}")
        print(f"Открытый ключ: {self.public_key}")
        
        return self.private_key, self.public_key
    
    def text_to_numbers(self, text: str) -> List[int]:
        """Преобразование текста в числа"""
        print(f"Преобразование текста '{text}' в числа...")
        
        # Простое преобразование: каждому символу соответствует его позиция в алфавите
        # A=1, B=2, ..., Z=26, пробел=27
        numbers = []
        for char in text:
            if char == ' ':
                numbers.append(27)
            elif char.isalpha():
                numbers.append(ord(char.upper()) - ord('A') + 1)
            else:
                # Для других символов используем их ASCII код по модулю 26
                numbers.append((ord(char) % 26) + 1)
        
        print(f"Результат: {numbers}")
        return numbers
    
    def numbers_to_text(self, numbers: List[int]) -> str:
        """Преобразование чисел в текст"""
        print(f"Преобразование чисел {numbers} в текст...")
        
        text = ""
        for num in numbers:
            if num == 27:
                text += ' '
            elif 1 <= num <= 26:
                text += chr(ord('A') + num - 1)
            else:
                # Для других чисел используем обратное преобразование
                text += chr((num - 1) % 26 + ord('A'))
        
        print(f"Результат: '{text}'")
        return text
    
    def encrypt(self, message: str, public_key: int) -> List[Tuple[int, int]]:
        """Шифрование сообщения"""
        print(f"Шифрование сообщения '{message}'...")
        
        # Преобразуем текст в числа
        numbers = self.text_to_numbers(message)
        
        encrypted = []
        for m in numbers:
            # Выбираем случайное k
            k = random.randrange(1, self.n)
            
            # Вычисляем c1 = alpha^k mod p
            c1 = pow(self.alpha, k, self.p)
            
            # Вычисляем c2 = m * (public_key^k) mod p
            c2 = (m * pow(public_key, k, self.p)) % self.p
            
            encrypted.append((c1, c2))
        
        print(f"Зашифрованное сообщение: {encrypted}")
        return encrypted
    
    def decrypt(self, encrypted: List[Tuple[int, int]]) -> str:
        """Расшифрование сообщения"""
        print(f"Расшифрование сообщения {encrypted}...")
        
        decrypted_numbers = []
        for c1, c2 in encrypted:
            # Вычисляем m = c2 * (c1^(p-1-private_key)) mod p
            # Это эквивалентно m = c2 * (c1^(-private_key)) mod p
            m = (c2 * pow(c1, self.p - 1 - self.private_key, self.p)) % self.p
            decrypted_numbers.append(m)
        
        # Преобразуем числа в текст
        message = self.numbers_to_text(decrypted_numbers)
        
        print(f"Расшифрованное сообщение: '{message}'")
        return message
    
    def sign(self, message: str) -> Tuple[int, int]:
        """Создание цифровой подписи"""
        print(f"Создание цифровой подписи для сообщения '{message}'...")
        
        # Преобразуем сообщение в число (хеш)
        message_hash = hash(message) % self.p
        if message_hash < 0:
            message_hash += self.p
        
        # Выбираем случайное k
        k = random.randrange(1, self.n)
        while math.gcd(k, self.n) != 1:
            k = random.randrange(1, self.n)
        
        # Вычисляем r = alpha^k mod p
        r = pow(self.alpha, k, self.p)
        
        # Вычисляем s = (message_hash - private_key * r) * k^(-1) mod n
        k_inv = self.modular_inverse(k, self.n)
        s = ((message_hash - self.private_key * r) * k_inv) % self.n
        
        signature = (r, s)
        print(f"Цифровая подпись: {signature}")
        return signature
    
    def verify_signature(self, message: str, signature: Tuple[int, int], public_key: int) -> bool:
        """Проверка цифровой подписи"""
        print(f"Проверка цифровой подписи {signature} для сообщения '{message}'...")
        
        r, s = signature
        
        # Преобразуем сообщение в число (хеш)
        message_hash = hash(message) % self.p
        if message_hash < 0:
            message_hash += self.p
        
        # Вычисляем v1 = alpha^message_hash mod p
        v1 = pow(self.alpha, message_hash, self.p)
        
        # Вычисляем v2 = (public_key^r * r^s) mod p
        v2 = (pow(public_key, r, self.p) * pow(r, s, self.p)) % self.p
        
        is_valid = v1 == v2
        print(f"Подпись {'валидна' if is_valid else 'невалидна'}")
        return is_valid
    
    def modular_inverse(self, a: int, m: int) -> int:
        """Вычисление модульного обратного элемента"""
        def extended_gcd(a, b):
            if a == 0:
                return b, 0, 1
            gcd, x1, y1 = extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y
        
        gcd, x, _ = extended_gcd(a, m)
        if gcd != 1:
            raise ValueError(f"Обратный элемент для {a} по модулю {m} не существует")
        
        return x % m


def main():
    """Основная функция программы"""
    print("=" * 60)
    print("РЕАЛИЗАЦИЯ АЛГОРИТМА ЭЛЬ-ГАМАЛЯ")
    print("Практическая работа №10 - Вариант 7")
    print("=" * 60)
    
    elgamal = ElGamal()
    
    # Ввод параметров
    print("\n1. ВВОД ПАРАМЕТРОВ")
    print("-" * 30)
    
    # Ввод p
    while True:
        try:
            p = int(input("Введите простое число p: "))
            if elgamal.check_prime(p):
                elgamal.p = p
                break
        except ValueError:
            print("❌ Введите корректное число")
    
    # Ввод n
    while True:
        try:
            n = int(input("Введите порядок группы n: "))
            alpha = int(input("Введите генератор группы alpha: "))
            if elgamal.check_parameters(p, n, alpha):
                elgamal.n = n
                elgamal.alpha = alpha
                break
        except ValueError:
            print("❌ Введите корректные числа")
    
    # Генерация ключей
    print("\n2. ГЕНЕРАЦИЯ КЛЮЧЕЙ")
    print("-" * 30)
    private_key, public_key = elgamal.generate_keys(p, n, alpha)
    
    # Ввод сообщения
    print("\n3. ШИФРОВАНИЕ И РАСШИФРОВАНИЕ")
    print("-" * 30)
    message = input("Введите сообщение для шифрования: ")
    
    # Шифрование
    encrypted = elgamal.encrypt(message, public_key)
    
    # Расшифрование
    decrypted = elgamal.decrypt(encrypted)
    
    print(f"\nИсходное сообщение: '{message}'")
    print(f"Расшифрованное сообщение: '{decrypted}'")
    print(f"Сообщения {'совпадают' if message == decrypted else 'не совпадают'}")
    
    # Цифровая подпись
    print("\n4. ЦИФРОВАЯ ПОДПИСЬ")
    print("-" * 30)
    sign_message = input("Введите сообщение для подписи: ")
    
    # Создание подписи
    signature = elgamal.sign(sign_message)
    
    # Проверка подписи
    is_valid = elgamal.verify_signature(sign_message, signature, public_key)
    
    print(f"\nСообщение: '{sign_message}'")
    print(f"Подпись: {signature}")
    print(f"Подпись {'валидна' if is_valid else 'невалидна'}")


if __name__ == "__main__":
    main()
