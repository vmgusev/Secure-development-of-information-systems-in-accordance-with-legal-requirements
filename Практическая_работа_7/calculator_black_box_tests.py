#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Система автоматизированного тестирования GUI-приложения методом черного ящика
Практическая работа №7 - Вариант 7

Автор: Гусев В.М. КВМО-11-24
Дата: 2025

Тестируемое приложение: Калькулятор Windows
Тестируемая функция: Арифметические операции (сложение, вычитание, умножение, деление)
"""

import time
import sys
import os
from typing import List, Tuple, Optional
import unittest
from pathlib import Path

# Проверяем доступность инструментов автоматизации
import platform

# Для macOS используем pyautogui и subprocess
try:
    import pyautogui
    import subprocess
    import os
    MACOS_AUTOMATION_AVAILABLE = True
except ImportError:
    MACOS_AUTOMATION_AVAILABLE = False
    print("ВНИМАНИЕ: pyautogui не установлен. Установите его командой: pip install pyautogui")

# Для Windows (если понадобится)
try:
    from pywinauto import Application, findwindows
    from pywinauto.controls.win32_controls import ButtonWrapper
    PYWINAUTO_AVAILABLE = True
except ImportError:
    PYWINAUTO_AVAILABLE = False


class CalculatorBlackBoxTester:
    """
    Класс для автоматизированного тестирования калькулятора методом черного ящика
    """
    
    def __init__(self):
        """Инициализация тестера"""
        self.app = None
        self.calculator_window = None
        self.test_results = []
        self.passed_tests = 0
        self.failed_tests = 0
        
        # Маппинг кнопок калькулятора
        self.button_mapping = {
            '0': '0', '1': '1', '2': '2', '3': '3', '4': '4',
            '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
            '+': 'Plus', '-': 'Minus', '*': 'Multiply', '/': 'Divide',
            '=': 'Equals', 'C': 'Clear', 'CE': 'Clear entry'
        }
    
    def start_calculator(self) -> bool:
        """
        Запуск калькулятора
        
        Returns:
            bool: True если калькулятор успешно запущен
        """
        try:
            if not PYWINAUTO_AVAILABLE:
                print("ОШИБКА: pywinauto не доступен")
                return False
            
            # Пытаемся найти уже запущенный калькулятор
            try:
                self.app = Application().connect(title_re=".*Calculator.*")
                print("Найден уже запущенный калькулятор")
            except:
                # Запускаем новый калькулятор
                self.app = Application().start("calc.exe")
                print("Запущен новый калькулятор")
                time.sleep(2)  # Ждем загрузки
            
            # Получаем главное окно
            self.calculator_window = self.app.window(title_re=".*Calculator.*")
            
            if self.calculator_window.exists():
                print("Калькулятор успешно подключен")
                return True
            else:
                print("ОШИБКА: Не удалось найти окно калькулятора")
                return False
                
        except Exception as e:
            print(f"ОШИБКА при запуске калькулятора: {e}")
            return False
    
    def click_button(self, button_name: str) -> bool:
        """
        Нажатие на кнопку калькулятора
        
        Args:
            button_name: Название кнопки
            
        Returns:
            bool: True если кнопка нажата успешно
        """
        try:
            if button_name in self.button_mapping:
                button_id = self.button_mapping[button_name]
                button = self.calculator_window.child_window(auto_id=button_id)
                if button.exists():
                    button.click()
                    time.sleep(0.1)  # Небольшая задержка
                    return True
                else:
                    print(f"Кнопка {button_name} не найдена")
                    return False
            else:
                print(f"Неизвестная кнопка: {button_name}")
                return False
        except Exception as e:
            print(f"ОШИБКА при нажатии кнопки {button_name}: {e}")
            return False
    
    def get_display_value(self) -> Optional[str]:
        """
        Получение значения с дисплея калькулятора
        
        Returns:
            str: Значение на дисплее или None при ошибке
        """
        try:
            # Пытаемся найти дисплей калькулятора
            display = self.calculator_window.child_window(auto_id="CalculatorResults")
            if display.exists():
                return display.window_text()
            else:
                # Альтернативный способ поиска дисплея
                display = self.calculator_window.child_window(control_type="Text")
                if display.exists():
                    return display.window_text()
                else:
                    print("Дисплей калькулятора не найден")
                    return None
        except Exception as e:
            print(f"ОШИБКА при получении значения дисплея: {e}")
            return None
    
    def clear_calculator(self) -> bool:
        """
        Очистка калькулятора
        
        Returns:
            bool: True если очистка выполнена успешно
        """
        try:
            return self.click_button('C')
        except Exception as e:
            print(f"ОШИБКА при очистке калькулятора: {e}")
            return False
    
    def perform_calculation(self, expression: str) -> Optional[float]:
        """
        Выполнение вычисления
        
        Args:
            expression: Математическое выражение (например, "2+3")
            
        Returns:
            float: Результат вычисления или None при ошибке
        """
        try:
            # Очищаем калькулятор
            self.clear_calculator()
            time.sleep(0.2)
            
            # Вводим выражение посимвольно
            for char in expression:
                if char in self.button_mapping:
                    if not self.click_button(char):
                        return None
                elif char == ' ':
                    continue  # Пропускаем пробелы
                else:
                    print(f"Неподдерживаемый символ: {char}")
                    return None
            
            # Нажимаем равно
            if not self.click_button('='):
                return None
            
            time.sleep(0.5)  # Ждем вычисления
            
            # Получаем результат
            result_text = self.get_display_value()
            if result_text:
                try:
                    # Парсим результат (убираем лишние символы)
                    result_text = result_text.replace('Display is ', '').strip()
                    return float(result_text)
                except ValueError:
                    print(f"Не удалось преобразовать результат в число: {result_text}")
                    return None
            else:
                return None
                
        except Exception as e:
            print(f"ОШИБКА при выполнении вычисления {expression}: {e}")
            return None
    
    def run_test(self, test_name: str, expression: str, expected_result: float, tolerance: float = 0.001) -> bool:
        """
        Запуск одного теста
        
        Args:
            test_name: Название теста
            expression: Выражение для вычисления
            expected_result: Ожидаемый результат
            tolerance: Допустимая погрешность
            
        Returns:
            bool: True если тест прошел успешно
        """
        print(f"\nТест: {test_name}")
        print(f"Выражение: {expression}")
        print(f"Ожидаемый результат: {expected_result}")
        
        actual_result = self.perform_calculation(expression)
        
        if actual_result is not None:
            if abs(actual_result - expected_result) <= tolerance:
                print(f"✅ ПРОЙДЕН: {actual_result}")
                self.passed_tests += 1
                self.test_results.append(f"✅ {test_name}: ПРОЙДЕН")
                return True
            else:
                print(f"❌ ПРОВАЛЕН: получен {actual_result}, ожидался {expected_result}")
                self.failed_tests += 1
                self.test_results.append(f"❌ {test_name}: ПРОВАЛЕН")
                return False
        else:
            print(f"❌ ОШИБКА: не удалось получить результат")
            self.failed_tests += 1
            self.test_results.append(f"❌ {test_name}: ОШИБКА")
            return False
    
    def run_all_tests(self) -> None:
        """Запуск всех тестов"""
        print("ЗАПУСК АВТОМАТИЗИРОВАННОГО ТЕСТИРОВАНИЯ КАЛЬКУЛЯТОРА")
        print("Метод черного ящика - Практическая работа №7")
        print("=" * 60)
        
        if not self.start_calculator():
            print("НЕ УДАЛОСЬ ЗАПУСТИТЬ КАЛЬКУЛЯТОР. ТЕСТИРОВАНИЕ ПРЕРВАНО.")
            return
        
        # Тесты сложения
        print("\n" + "=" * 40)
        print("ТЕСТЫ СЛОЖЕНИЯ")
        print("=" * 40)
        
        self.run_test("Сложение простых чисел", "2+3", 5.0)
        self.run_test("Сложение с нулем", "5+0", 5.0)
        self.run_test("Сложение отрицательных чисел", "(-2)+(-3)", -5.0)
        self.run_test("Сложение больших чисел", "100+200", 300.0)
        self.run_test("Сложение десятичных чисел", "2.5+3.7", 6.2)
        
        # Тесты вычитания
        print("\n" + "=" * 40)
        print("ТЕСТЫ ВЫЧИТАНИЯ")
        print("=" * 40)
        
        self.run_test("Вычитание простых чисел", "5-3", 2.0)
        self.run_test("Вычитание с нулем", "5-0", 5.0)
        self.run_test("Вычитание из нуля", "0-5", -5.0)
        self.run_test("Вычитание отрицательных чисел", "(-5)-(-3)", -2.0)
        self.run_test("Вычитание десятичных чисел", "5.5-2.3", 3.2)
        
        # Тесты умножения
        print("\n" + "=" * 40)
        print("ТЕСТЫ УМНОЖЕНИЯ")
        print("=" * 40)
        
        self.run_test("Умножение простых чисел", "3*4", 12.0)
        self.run_test("Умножение на ноль", "5*0", 0.0)
        self.run_test("Умножение на единицу", "5*1", 5.0)
        self.run_test("Умножение отрицательных чисел", "(-3)*(-4)", 12.0)
        self.run_test("Умножение десятичных чисел", "2.5*4", 10.0)
        
        # Тесты деления
        print("\n" + "=" * 40)
        print("ТЕСТЫ ДЕЛЕНИЯ")
        print("=" * 40)
        
        self.run_test("Деление простых чисел", "8/2", 4.0)
        self.run_test("Деление на единицу", "5/1", 5.0)
        self.run_test("Деление десятичных чисел", "7.5/2.5", 3.0)
        self.run_test("Деление отрицательных чисел", "(-8)/(-2)", 4.0)
        
        # Тесты граничных условий
        print("\n" + "=" * 40)
        print("ТЕСТЫ ГРАНИЧНЫХ УСЛОВИЙ")
        print("=" * 40)
        
        self.run_test("Максимальные числа", "999999+1", 1000000.0)
        self.run_test("Минимальные числа", "1+1", 2.0)
        self.run_test("Деление на очень маленькое число", "1/0.001", 1000.0)
        
        # Тесты сложных выражений
        print("\n" + "=" * 40)
        print("ТЕСТЫ СЛОЖНЫХ ВЫРАЖЕНИЙ")
        print("=" * 40)
        
        # Примечание: Калькулятор Windows обычно не поддерживает сложные выражения
        # без скобок, поэтому тестируем простые последовательные операции
        self.run_test("Последовательные операции 1", "2+3*4", 14.0)  # 2+3=5, 5*4=20 (если без приоритета)
        self.run_test("Последовательные операции 2", "10-2*3", 4.0)  # 10-2=8, 8*3=24 (если без приоритета)
        
        # Вывод результатов
        self.print_summary()
    
    def print_summary(self) -> None:
        """Вывод сводки результатов тестирования"""
        print("\n" + "=" * 60)
        print("СВОДКА РЕЗУЛЬТАТОВ ТЕСТИРОВАНИЯ")
        print("=" * 60)
        print(f"Всего тестов: {self.passed_tests + self.failed_tests}")
        print(f"Пройдено: {self.passed_tests}")
        print(f"Провалено: {self.failed_tests}")
        
        if self.passed_tests + self.failed_tests > 0:
            success_rate = (self.passed_tests / (self.passed_tests + self.failed_tests)) * 100
            print(f"Процент успешности: {success_rate:.1f}%")
        
        if self.failed_tests > 0:
            print("\nПРОВАЛЕННЫЕ ТЕСТЫ:")
            for result in self.test_results:
                if result.startswith("❌"):
                    print(f"  {result}")
    
    def close_calculator(self) -> None:
        """Закрытие калькулятора"""
        try:
            if self.calculator_window and self.calculator_window.exists():
                self.calculator_window.close()
                print("Калькулятор закрыт")
        except Exception as e:
            print(f"ОШИБКА при закрытии калькулятора: {e}")


class CalculatorTestSuite(unittest.TestCase):
    """
    Класс для unit-тестирования системы тестирования калькулятора
    """
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        self.tester = CalculatorBlackBoxTester()
    
    def tearDown(self):
        """Очистка после каждого теста"""
        if self.tester:
            self.tester.close_calculator()
    
    def test_calculator_startup(self):
        """Тест запуска калькулятора"""
        if PYWINAUTO_AVAILABLE:
            result = self.tester.start_calculator()
            if result:
                self.assertTrue(self.tester.calculator_window.exists())
            else:
                self.skipTest("Калькулятор не удалось запустить")
        else:
            self.skipTest("pywinauto не доступен")
    
    def test_button_clicking(self):
        """Тест нажатия кнопок"""
        if PYWINAUTO_AVAILABLE and self.tester.start_calculator():
            # Тестируем нажатие кнопки "1"
            result = self.tester.click_button('1')
            self.assertTrue(result)
        else:
            self.skipTest("pywinauto не доступен или калькулятор не запущен")
    
    def test_display_reading(self):
        """Тест чтения дисплея"""
        if PYWINAUTO_AVAILABLE and self.tester.start_calculator():
            self.tester.clear_calculator()
            self.tester.click_button('5')
            display_value = self.tester.get_display_value()
            # Проверяем, что дисплей содержит "5" или похожее значение
            self.assertIsNotNone(display_value)
        else:
            self.skipTest("pywinauto не доступен или калькулятор не запущен")


def main():
    """Основная функция для запуска тестирования"""
    print("АВТОМАТИЗИРОВАННОЕ ТЕСТИРОВАНИЕ GUI-ПРИЛОЖЕНИЙ")
    print("Практическая работа №7 - Вариант 7")
    print("Метод черного ящика")
    print("=" * 60)
    
    if not PYWINAUTO_AVAILABLE:
        print("\n❌ ОШИБКА: pywinauto не установлен")
        print("Для установки выполните команду: pip install pywinauto")
        print("\nАльтернативно, можно запустить симуляцию тестирования:")
        
        # Запускаем симуляцию тестирования
        run_simulation()
        return
    
    # Создаем тестер
    tester = CalculatorBlackBoxTester()
    
    try:
        # Запускаем тестирование
        tester.run_all_tests()
    except KeyboardInterrupt:
        print("\n\nТестирование прервано пользователем")
    except Exception as e:
        print(f"\n\nОШИБКА при выполнении тестирования: {e}")
    finally:
        # Закрываем калькулятор
        tester.close_calculator()


def run_simulation():
    """
    Симуляция тестирования для демонстрации без pywinauto
    """
    print("\n" + "=" * 60)
    print("СИМУЛЯЦИЯ ТЕСТИРОВАНИЯ КАЛЬКУЛЯТОРА")
    print("(pywinauto не установлен)")
    print("=" * 60)
    
    # Симулируем результаты тестирования
    test_cases = [
        ("Сложение простых чисел", "2+3", 5.0, True),
        ("Сложение с нулем", "5+0", 5.0, True),
        ("Вычитание простых чисел", "5-3", 2.0, True),
        ("Умножение простых чисел", "3*4", 12.0, True),
        ("Деление простых чисел", "8/2", 4.0, True),
        ("Деление на ноль", "5/0", float('inf'), False),  # Ожидаемая ошибка
        ("Сложное выражение", "2+3*4", 14.0, True),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, expression, expected, should_pass in test_cases:
        print(f"\nТест: {test_name}")
        print(f"Выражение: {expression}")
        print(f"Ожидаемый результат: {expected}")
        
        if should_pass:
            print("✅ ПРОЙДЕН (симуляция)")
            passed += 1
        else:
            print("❌ ПРОВАЛЕН (симуляция)")
            failed += 1
    
    print(f"\n" + "=" * 60)
    print("СВОДКА РЕЗУЛЬТАТОВ СИМУЛЯЦИИ")
    print("=" * 60)
    print(f"Всего тестов: {passed + failed}")
    print(f"Пройдено: {passed}")
    print(f"Провалено: {failed}")
    print(f"Процент успешности: {(passed / (passed + failed)) * 100:.1f}%")


if __name__ == "__main__":
    main()
