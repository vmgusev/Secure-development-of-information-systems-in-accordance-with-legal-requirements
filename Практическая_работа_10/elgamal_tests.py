#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тесты для алгоритма Эль-Гамаля
Практическая работа №10 - Вариант 7
"""

import unittest
from elgamal_implementation import ElGamal


class TestElGamal(unittest.TestCase):
    """Тесты для класса ElGamal"""
    
    def setUp(self):
        """Настройка тестов"""
        self.elgamal = ElGamal()
        self.elgamal.p = 23
        self.elgamal.n = 11
        self.elgamal.alpha = 2
        self.elgamal.private_key = 7
        self.elgamal.public_key = 13
    
    def test_is_prime(self):
        """Тест проверки простоты чисел"""
        # Простые числа
        self.assertTrue(self.elgamal.is_prime(2))
        self.assertTrue(self.elgamal.is_prime(3))
        self.assertTrue(self.elgamal.is_prime(17))
        self.assertTrue(self.elgamal.is_prime(23))
        
        # Составные числа
        self.assertFalse(self.elgamal.is_prime(1))
        self.assertFalse(self.elgamal.is_prime(4))
        self.assertFalse(self.elgamal.is_prime(15))
        self.assertFalse(self.elgamal.is_prime(25))
    
    def test_miller_rabin_test(self):
        """Тест Миллера-Рабина"""
        # Простые числа
        self.assertTrue(self.elgamal.miller_rabin_test(2))
        self.assertTrue(self.elgamal.miller_rabin_test(3))
        self.assertTrue(self.elgamal.miller_rabin_test(17))
        
        # Составные числа
        self.assertFalse(self.elgamal.miller_rabin_test(1))
        self.assertFalse(self.elgamal.miller_rabin_test(4))
        self.assertFalse(self.elgamal.miller_rabin_test(15))
    
    def test_fermat_test(self):
        """Тест Ферма"""
        # Простые числа
        self.assertTrue(self.elgamal.fermat_test(2))
        self.assertTrue(self.elgamal.fermat_test(3))
        self.assertTrue(self.elgamal.fermat_test(17))
        
        # Составные числа
        self.assertFalse(self.elgamal.fermat_test(1))
        self.assertFalse(self.elgamal.fermat_test(4))
        self.assertFalse(self.elgamal.fermat_test(15))
    
    def test_check_parameters(self):
        """Тест проверки параметров"""
        # Корректные параметры
        self.assertTrue(self.elgamal.check_parameters(23, 11, 2))
        
        # Некорректные параметры
        self.assertFalse(self.elgamal.check_parameters(23, 12, 2))  # n не делит p-1
        # Проверим с alpha=1, который точно не подходит
        self.assertFalse(self.elgamal.check_parameters(23, 11, 1))  # alpha=1 не подходит
    
    def test_text_to_numbers(self):
        """Тест преобразования текста в числа"""
        result = self.elgamal.text_to_numbers("ABC")
        expected = [1, 2, 3]  # A=1, B=2, C=3
        self.assertEqual(result, expected)
    
    def test_numbers_to_text(self):
        """Тест преобразования чисел в текст"""
        result = self.elgamal.numbers_to_text([1, 2, 3])
        expected = "ABC"
        self.assertEqual(result, expected)
    
    def test_modular_inverse(self):
        """Тест вычисления модульного обратного"""
        # Тест для простых случаев
        self.assertEqual(self.elgamal.modular_inverse(3, 11), 4)  # 3 * 4 = 12 ≡ 1 (mod 11)
        self.assertEqual(self.elgamal.modular_inverse(7, 11), 8)  # 7 * 8 = 56 ≡ 1 (mod 11)
        
        # Тест для случая, когда обратный не существует
        with self.assertRaises(ValueError):
            self.elgamal.modular_inverse(2, 4)  # gcd(2, 4) = 2 != 1
    
    def test_encrypt_decrypt(self):
        """Тест шифрования и расшифрования"""
        message = "HELLO"
        
        # Генерируем правильные ключи
        private_key, public_key = self.elgamal.generate_keys(23, 11, 2)
        
        # Шифрование
        encrypted = self.elgamal.encrypt(message, public_key)
        
        # Расшифрование
        decrypted = self.elgamal.decrypt(encrypted)
        
        self.assertEqual(message, decrypted)
    
    def test_sign_verify(self):
        """Тест создания и проверки цифровой подписи"""
        message = "TEST"
        
        # Создание подписи
        signature = self.elgamal.sign(message)
        
        # Проверка подписи
        is_valid = self.elgamal.verify_signature(message, signature, self.elgamal.public_key)
        
        self.assertTrue(is_valid)
    
    def test_sign_verify_invalid(self):
        """Тест проверки невалидной подписи"""
        message = "TEST"
        
        # Создание подписи
        signature = self.elgamal.sign(message)
        
        # Изменяем сообщение
        modified_message = "WRONG"
        
        # Проверка подписи для измененного сообщения
        is_valid = self.elgamal.verify_signature(modified_message, signature, self.elgamal.public_key)
        
        self.assertFalse(is_valid)
    
    def test_generate_keys(self):
        """Тест генерации ключей"""
        private_key, public_key = self.elgamal.generate_keys(23, 11, 2)
        
        # Проверяем, что ключи в правильном диапазоне
        self.assertGreaterEqual(private_key, 1)
        self.assertLess(private_key, 11)
        self.assertGreaterEqual(public_key, 1)
        self.assertLess(public_key, 23)
        
        # Проверяем, что открытый ключ вычислен правильно
        expected_public_key = pow(2, private_key, 23)
        self.assertEqual(public_key, expected_public_key)


def run_tests():
    """Запуск всех тестов"""
    print("=" * 60)
    print("ТЕСТИРОВАНИЕ АЛГОРИТМА ЭЛЬ-ГАМАЛЯ")
    print("=" * 60)
    
    # Создаем тестовый набор
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestElGamal)
    
    # Запускаем тесты
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Выводим результаты
    print(f"\nРезультаты тестирования:")
    print(f"Тестов выполнено: {result.testsRun}")
    print(f"Успешно: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Неудачно: {len(result.failures)}")
    print(f"Ошибок: {len(result.errors)}")
    
    if result.failures:
        print("\nНеудачные тесты:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nОшибки:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    run_tests()
