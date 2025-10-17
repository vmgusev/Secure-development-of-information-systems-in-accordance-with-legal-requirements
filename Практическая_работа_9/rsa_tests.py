#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тесты для реализации алгоритма RSA
Практическая работа №9 - Вариант 7

Автор: Гусев В.М. КВМО-11-24
Дата: 2025

Тестирует все функции RSA на корректность работы
"""

from rsa_implementation import RSAImplementation


class RSATests:
    """Класс для тестирования RSA"""
    
    def __init__(self):
        self.rsa = RSAImplementation()
        self.tests_passed = 0
        self.tests_failed = 0
    
    def assert_equal(self, actual, expected, test_name):
        """Проверка равенства значений"""
        if actual == expected:
            print(f"✓ {test_name}: PASSED")
            self.tests_passed += 1
            return True
        else:
            print(f"✗ {test_name}: FAILED (ожидалось {expected}, получено {actual})")
            self.tests_failed += 1
            return False
    
    def assert_true(self, condition, test_name):
        """Проверка истинности условия"""
        if condition:
            print(f"✓ {test_name}: PASSED")
            self.tests_passed += 1
            return True
        else:
            print(f"✗ {test_name}: FAILED")
            self.tests_failed += 1
            return False
    
    def test_prime_detection(self):
        """Тестирование определения простых чисел"""
        print("\nТЕСТИРОВАНИЕ ОПРЕДЕЛЕНИЯ ПРОСТЫХ ЧИСЕЛ")
        print("=" * 50)
        
        # Простые числа
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        
        for prime in primes:
            result = self.rsa.check_prime(prime)
            self.assert_true(result['is_prime'], f"Число {prime} должно быть простым")
        
        # Составные числа
        composites = [4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 26, 27, 28, 30, 32, 33, 34, 35, 36, 38, 39, 40, 42, 44, 45, 46, 48, 49, 50]
        
        for composite in composites:
            result = self.rsa.check_prime(composite)
            self.assert_true(not result['is_prime'], f"Число {composite} должно быть составным")
    
    def test_gcd(self):
        """Тестирование алгоритма Евклида"""
        print("\nТЕСТИРОВАНИЕ АЛГОРИТМА ЕВКЛИДА")
        print("=" * 50)
        
        test_cases = [
            (12, 8, 4),
            (15, 25, 5),
            (17, 13, 1),
            (100, 50, 50),
            (7, 11, 1),
            (24, 36, 12),
            (1, 1, 1),
            (0, 5, 5),
            (5, 0, 5)
        ]
        
        for a, b, expected in test_cases:
            actual = self.rsa.gcd(a, b)
            self.assert_equal(actual, expected, f"НОД({a}, {b})")
    
    def test_extended_gcd(self):
        """Тестирование расширенного алгоритма Евклида"""
        print("\nТЕСТИРОВАНИЕ РАСШИРЕННОГО АЛГОРИТМА ЕВКЛИДА")
        print("=" * 50)
        
        test_cases = [
            (12, 8),
            (15, 25),
            (17, 13),
            (7, 11),
            (24, 36)
        ]
        
        for a, b in test_cases:
            gcd, x, y = self.rsa.extended_gcd(a, b)
            # Проверяем, что ax + by = gcd
            result = a * x + b * y
            self.assert_equal(result, gcd, f"Расширенный НОД({a}, {b}): {a}*{x} + {b}*{y} = {result}")
    
    def test_modular_inverse(self):
        """Тестирование нахождения обратного элемента"""
        print("\nТЕСТИРОВАНИЕ НАХОЖДЕНИЯ ОБРАТНОГО ЭЛЕМЕНТА")
        print("=" * 50)
        
        test_cases = [
            (3, 7),   # 3^(-1) mod 7 = 5
            (5, 11),  # 5^(-1) mod 11 = 9
            (7, 13),  # 7^(-1) mod 13 = 2
            (2, 5),   # 2^(-1) mod 5 = 3
            (4, 9)    # 4^(-1) mod 9 = 7
        ]
        
        for a, m in test_cases:
            inv = self.rsa.modular_inverse(a, m)
            if inv is not None:
                # Проверяем, что a * inv ≡ 1 (mod m)
                result = (a * inv) % m
                self.assert_equal(result, 1, f"{a}^(-1) mod {m} = {inv}")
            else:
                print(f"✗ Обратный элемент для {a} mod {m} не найден")
                self.tests_failed += 1
    
    def test_modular_exponentiation(self):
        """Тестирование быстрого возведения в степень"""
        print("\nТЕСТИРОВАНИЕ БЫСТРОГО ВОЗВЕДЕНИЯ В СТЕПЕНЬ")
        print("=" * 50)
        
        test_cases = [
            (2, 3, 5, 3),    # 2^3 mod 5 = 3
            (3, 4, 7, 4),    # 3^4 mod 7 = 4
            (5, 2, 11, 3),   # 5^2 mod 11 = 3
            (7, 3, 13, 5),   # 7^3 mod 13 = 5
            (2, 10, 11, 1)   # 2^10 mod 11 = 1
        ]
        
        for base, exp, mod, expected in test_cases:
            actual = self.rsa.modular_exponentiation(base, exp, mod)
            self.assert_equal(actual, expected, f"{base}^{exp} mod {mod}")
    
    def test_text_conversion(self):
        """Тестирование преобразования текста в числа и обратно"""
        print("\nТЕСТИРОВАНИЕ ПРЕОБРАЗОВАНИЯ ТЕКСТА")
        print("=" * 50)
        
        test_messages = [
            "Hello",
            "RSA",
            "Test123",
            "АБВ",
            "Криптография",
            "!@#$%",
            "",
            "A",
            "1234567890"
        ]
        
        for message in test_messages:
            numbers = self.rsa.text_to_numbers(message)
            restored = self.rsa.numbers_to_text(numbers)
            self.assert_equal(restored, message, f"Преобразование '{message}'")
    
    def test_key_generation(self):
        """Тестирование генерации ключей"""
        print("\nТЕСТИРОВАНИЕ ГЕНЕРАЦИИ КЛЮЧЕЙ")
        print("=" * 50)
        
        # Тест 1: Маленькие простые числа
        success = self.rsa.generate_keys(11, 13)
        self.assert_true(success, "Генерация ключей для p=11, q=13")
        
        if success:
            # Проверяем корректность ключей
            self.assert_equal(self.rsa.n, 143, "n = p * q")
            self.assert_equal(self.rsa.phi, 120, "φ(n) = (p-1)(q-1)")
            self.assert_true(self.rsa.gcd(self.rsa.e, self.rsa.phi) == 1, "НОД(e, φ(n)) = 1")
            self.assert_equal((self.rsa.e * self.rsa.d) % self.rsa.phi, 1, "e * d ≡ 1 (mod φ(n))")
        
        # Тест 2: Другие простые числа
        success2 = self.rsa.generate_keys(17, 19)
        self.assert_true(success2, "Генерация ключей для p=17, q=19")
        
        if success2:
            self.assert_equal(self.rsa.n, 323, "n = p * q")
            self.assert_equal(self.rsa.phi, 288, "φ(n) = (p-1)(q-1)")
    
    def test_encryption_decryption(self):
        """Тестирование шифрования и расшифрования"""
        print("\nТЕСТИРОВАНИЕ ШИФРОВАНИЯ И РАСШИФРОВАНИЯ")
        print("=" * 50)
        
        # Генерируем ключи
        success = self.rsa.generate_keys(11, 13)
        self.assert_true(success, "Генерация ключей для тестирования")
        
        if not success:
            return
        
        test_messages = ["Hi", "RSA", "Test", "123", "A", "Hello World!"]
        
        for message in test_messages:
            # Шифруем открытым ключом
            encrypted = self.rsa.encrypt(message, self.rsa.public_key)
            
            # Расшифровываем закрытым ключом
            decrypted = self.rsa.decrypt(encrypted, self.rsa.private_key)
            
            self.assert_equal(decrypted, message, f"Шифрование/расшифрование '{message}'")
    
    def test_rsa_properties(self):
        """Тестирование свойств RSA"""
        print("\nТЕСТИРОВАНИЕ СВОЙСТВ RSA")
        print("=" * 50)
        
        # Генерируем ключи
        success = self.rsa.generate_keys(11, 13)
        self.assert_true(success, "Генерация ключей для тестирования свойств")
        
        if not success:
            return
        
        message = "Test"
        
        # Свойство 1: Шифрование открытым ключом, расшифрование закрытым
        encrypted_public = self.rsa.encrypt(message, self.rsa.public_key)
        decrypted_private = self.rsa.decrypt(encrypted_public, self.rsa.private_key)
        self.assert_equal(decrypted_private, message, "Свойство 1: Открытый → Закрытый")
        
        # Свойство 2: Шифрование закрытым ключом, расшифрование открытым
        encrypted_private = self.rsa.encrypt(message, self.rsa.private_key)
        decrypted_public = self.rsa.decrypt(encrypted_private, self.rsa.public_key)
        self.assert_equal(decrypted_public, message, "Свойство 2: Закрытый → Открытый")
        
        # Свойство 3: Нельзя расшифровать тем же ключом
        encrypted_public2 = self.rsa.encrypt(message, self.rsa.public_key)
        decrypted_same = self.rsa.decrypt(encrypted_public2, self.rsa.public_key)
        self.assert_true(decrypted_same != message, "Свойство 3: Нельзя расшифровать тем же ключом")
    
    def test_error_handling(self):
        """Тестирование обработки ошибок"""
        print("\nТЕСТИРОВАНИЕ ОБРАБОТКИ ОШИБОК")
        print("=" * 50)
        
        # Тест 1: Составные числа
        success = self.rsa.generate_keys(15, 21)
        self.assert_true(not success, "Ошибка при использовании составных чисел")
        
        # Тест 2: Неподходящее значение e
        success = self.rsa.generate_keys(11, 13, 12)  # 12 не взаимно просто с φ(143)=120
        self.assert_true(not success, "Ошибка при неподходящем значении e")
        
        # Тест 3: Одинаковые простые числа
        success = self.rsa.generate_keys(11, 11)
        self.assert_true(not success, "Ошибка при одинаковых простых числах")
    
    def run_all_tests(self):
        """Запуск всех тестов"""
        print("ТЕСТИРОВАНИЕ РЕАЛИЗАЦИИ RSA")
        print("Практическая работа №9 - Вариант 7")
        print("=" * 60)
        
        self.test_prime_detection()
        self.test_gcd()
        self.test_extended_gcd()
        self.test_modular_inverse()
        self.test_modular_exponentiation()
        self.test_text_conversion()
        self.test_key_generation()
        self.test_encryption_decryption()
        self.test_rsa_properties()
        self.test_error_handling()
        
        print("\n" + "=" * 60)
        print("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
        print("=" * 60)
        print(f"Пройдено тестов: {self.tests_passed}")
        print(f"Провалено тестов: {self.tests_failed}")
        print(f"Всего тестов: {self.tests_passed + self.tests_failed}")
        print(f"Процент успеха: {(self.tests_passed / (self.tests_passed + self.tests_failed) * 100):.1f}%")
        
        if self.tests_failed == 0:
            print("\n🎉 Все тесты прошли успешно!")
        else:
            print(f"\n⚠️  {self.tests_failed} тестов провалено")


def main():
    """Основная функция тестирования"""
    tester = RSATests()
    tester.run_all_tests()


if __name__ == "__main__":
    main()
