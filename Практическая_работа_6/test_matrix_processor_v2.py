#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Система модульного тестирования для MatrixProcessorV2
Практическая работа №6 - Вариант 7

Автор: Гусев В.М. КВМО-11-24
Дата: 2025

Использует стандартную библиотеку unittest для тестирования
"""

import unittest
import sys
import os
from pathlib import Path

# Добавляем путь к модулю для импорта
sys.path.insert(0, str(Path(__file__).parent))

from matrix_processor_v2 import MatrixProcessorV2


class TestMatrixProcessorV2(unittest.TestCase):
    """
    Класс для тестирования MatrixProcessorV2
    """
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        self.processor = MatrixProcessorV2()
    
    def tearDown(self):
        """Очистка после каждого теста"""
        self.processor.reset()
    
    # Тесты создания матрицы
    
    def test_create_matrix_valid_size_2(self):
        """Тест создания матрицы размера 2x2"""
        result = self.processor.create_matrix(2)
        self.assertTrue(result)
        self.assertEqual(self.processor.get_size(), 2)
        self.assertIsNotNone(self.processor.get_matrix())
    
    def test_create_matrix_valid_size_5(self):
        """Тест создания матрицы размера 5x5"""
        result = self.processor.create_matrix(5)
        self.assertTrue(result)
        self.assertEqual(self.processor.get_size(), 5)
        self.assertIsNotNone(self.processor.get_matrix())
    
    def test_create_matrix_invalid_size_1(self):
        """Тест создания матрицы недопустимого размера 1"""
        result = self.processor.create_matrix(1)
        self.assertFalse(result)
        self.assertEqual(self.processor.get_size(), 0)
    
    def test_create_matrix_invalid_size_6(self):
        """Тест создания матрицы недопустимого размера 6"""
        result = self.processor.create_matrix(6)
        self.assertFalse(result)
        self.assertEqual(self.processor.get_size(), 0)
    
    def test_create_matrix_invalid_size_negative(self):
        """Тест создания матрицы с отрицательным размером"""
        result = self.processor.create_matrix(-2)
        self.assertFalse(result)
        self.assertEqual(self.processor.get_size(), 0)
    
    def test_create_matrix_invalid_size_float(self):
        """Тест создания матрицы с размером типа float"""
        result = self.processor.create_matrix(3.5)
        self.assertFalse(result)
        self.assertEqual(self.processor.get_size(), 0)
    
    def test_create_matrix_with_valid_values(self):
        """Тест создания матрицы с корректными пользовательскими значениями"""
        values = [[1, 2], [3, 4]]
        result = self.processor.create_matrix(2, values)
        self.assertTrue(result)
        self.assertEqual(self.processor.get_matrix(), values)
    
    def test_create_matrix_with_invalid_values_wrong_size(self):
        """Тест создания матрицы с неверным размером значений"""
        values = [[1, 2, 3], [4, 5]]  # Неправильный размер
        result = self.processor.create_matrix(2, values)
        self.assertFalse(result)
    
    def test_create_matrix_with_invalid_values_out_of_range(self):
        """Тест создания матрицы со значениями вне диапазона"""
        values = [[1, 2], [101, 4]]  # 101 вне диапазона [1, 100]
        result = self.processor.create_matrix(2, values)
        self.assertFalse(result)
    
    def test_create_matrix_with_invalid_values_wrong_type(self):
        """Тест создания матрицы с неверным типом значений"""
        values = [[1, 2], ["3", 4]]  # "3" не является int
        result = self.processor.create_matrix(2, values)
        self.assertFalse(result)
    
    # Тесты работы с элементами
    
    def test_get_element_valid_coordinates(self):
        """Тест получения элемента по корректным координатам"""
        self.processor.create_matrix(3)
        element = self.processor.get_element(1, 1)
        self.assertIsNotNone(element)
        self.assertIsInstance(element, int)
        self.assertGreaterEqual(element, 1)
        self.assertLessEqual(element, 100)
    
    def test_get_element_invalid_coordinates(self):
        """Тест получения элемента по неверным координатам"""
        self.processor.create_matrix(2)
        element = self.processor.get_element(5, 5)  # Координаты вне матрицы
        self.assertIsNone(element)
    
    def test_get_element_no_matrix(self):
        """Тест получения элемента когда матрица не создана"""
        element = self.processor.get_element(0, 0)
        self.assertIsNone(element)
    
    def test_set_element_valid(self):
        """Тест установки корректного значения элемента"""
        self.processor.create_matrix(2)
        result = self.processor.set_element(0, 1, 50)
        self.assertTrue(result)
        self.assertEqual(self.processor.get_element(0, 1), 50)
    
    def test_set_element_invalid_coordinates(self):
        """Тест установки элемента по неверным координатам"""
        self.processor.create_matrix(2)
        result = self.processor.set_element(5, 5, 50)
        self.assertFalse(result)
    
    def test_set_element_invalid_value(self):
        """Тест установки неверного значения элемента"""
        self.processor.create_matrix(2)
        result = self.processor.set_element(0, 0, 101)  # Значение вне диапазона
        self.assertFalse(result)
    
    def test_set_element_no_matrix(self):
        """Тест установки элемента когда матрица не создана"""
        result = self.processor.set_element(0, 0, 50)
        self.assertFalse(result)
    
    # Тесты обработки матрицы
    
    def test_process_matrix_2x2(self):
        """Тест обработки матрицы 2x2"""
        values = [[10, 20], [30, 40]]
        self.processor.create_matrix(2, values)
        
        result = self.processor.process_matrix()
        self.assertTrue(result)
        
        # Проверяем, что элементы ниже диагонали отсортированы
        self.assertTrue(self.processor.is_sorted_below_diagonal())
        
        # Проверяем, что элементы на диагонали и выше отрицательные
        self.assertTrue(self.processor.are_above_diagonal_negative())
    
    def test_process_matrix_3x3(self):
        """Тест обработки матрицы 3x3"""
        values = [[10, 20, 30], [40, 50, 60], [70, 80, 90]]
        self.processor.create_matrix(3, values)
        
        result = self.processor.process_matrix()
        self.assertTrue(result)
        
        # Проверяем, что элементы ниже диагонали отсортированы
        self.assertTrue(self.processor.is_sorted_below_diagonal())
        
        # Проверяем, что элементы на диагонали и выше отрицательные
        self.assertTrue(self.processor.are_above_diagonal_negative())
    
    def test_process_matrix_4x4(self):
        """Тест обработки матрицы 4x4"""
        values = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
        self.processor.create_matrix(4, values)
        
        result = self.processor.process_matrix()
        self.assertTrue(result)
        
        # Проверяем, что элементы ниже диагонали отсортированы
        self.assertTrue(self.processor.is_sorted_below_diagonal())
        
        # Проверяем, что элементы на диагонали и выше отрицательные
        self.assertTrue(self.processor.are_above_diagonal_negative())
    
    def test_process_matrix_5x5(self):
        """Тест обработки матрицы 5x5"""
        values = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15], 
                 [16, 17, 18, 19, 20], [21, 22, 23, 24, 25]]
        self.processor.create_matrix(5, values)
        
        result = self.processor.process_matrix()
        self.assertTrue(result)
        
        # Проверяем, что элементы ниже диагонали отсортированы
        self.assertTrue(self.processor.is_sorted_below_diagonal())
        
        # Проверяем, что элементы на диагонали и выше отрицательные
        self.assertTrue(self.processor.are_above_diagonal_negative())
    
    def test_process_matrix_no_matrix(self):
        """Тест обработки когда матрица не создана"""
        result = self.processor.process_matrix()
        self.assertFalse(result)
    
    # Тесты получения элементов
    
    def test_get_elements_below_diagonal_2x2(self):
        """Тест получения элементов ниже диагонали для матрицы 2x2"""
        values = [[1, 2], [3, 4]]
        self.processor.create_matrix(2, values)
        elements = self.processor.get_elements_below_diagonal()
        self.assertEqual(elements, [3])
    
    def test_get_elements_below_diagonal_3x3(self):
        """Тест получения элементов ниже диагонали для матрицы 3x3"""
        values = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.processor.create_matrix(3, values)
        elements = self.processor.get_elements_below_diagonal()
        self.assertEqual(elements, [4, 7, 8])
    
    def test_get_elements_below_diagonal_no_matrix(self):
        """Тест получения элементов ниже диагонали когда матрица не создана"""
        elements = self.processor.get_elements_below_diagonal()
        self.assertEqual(elements, [])
    
    def test_get_elements_above_and_on_diagonal_2x2(self):
        """Тест получения элементов на диагонали и выше для матрицы 2x2"""
        values = [[1, 2], [3, 4]]
        self.processor.create_matrix(2, values)
        elements = self.processor.get_elements_above_and_on_diagonal()
        self.assertEqual(elements, [1, 2, 4])
    
    def test_get_elements_above_and_on_diagonal_3x3(self):
        """Тест получения элементов на диагонали и выше для матрицы 3x3"""
        values = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.processor.create_matrix(3, values)
        elements = self.processor.get_elements_above_and_on_diagonal()
        self.assertEqual(elements, [1, 2, 3, 5, 6, 9])
    
    def test_get_elements_above_and_on_diagonal_no_matrix(self):
        """Тест получения элементов на диагонали и выше когда матрица не создана"""
        elements = self.processor.get_elements_above_and_on_diagonal()
        self.assertEqual(elements, [])
    
    # Тесты проверки результатов
    
    def test_is_sorted_below_diagonal_sorted(self):
        """Тест проверки сортировки для уже отсортированной матрицы"""
        values = [[1, 2], [3, 4]]
        self.processor.create_matrix(2, values)
        self.processor.process_matrix()
        self.assertTrue(self.processor.is_sorted_below_diagonal())
    
    def test_is_sorted_below_diagonal_not_sorted(self):
        """Тест проверки сортировки для неотсортированной матрицы"""
        values = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]  # Элементы ниже диагонали: [4, 7, 8] - не отсортированы по убыванию
        self.processor.create_matrix(3, values)
        # Не вызываем process_matrix()
        self.assertFalse(self.processor.is_sorted_below_diagonal())
    
    def test_is_sorted_below_diagonal_no_matrix(self):
        """Тест проверки сортировки когда матрица не создана"""
        self.assertTrue(self.processor.is_sorted_below_diagonal())  # Должно возвращать True для пустой матрицы
    
    def test_are_above_diagonal_negative_after_processing(self):
        """Тест проверки отрицательности элементов на диагонали и выше после обработки"""
        values = [[1, 2], [3, 4]]
        self.processor.create_matrix(2, values)
        self.processor.process_matrix()
        self.assertTrue(self.processor.are_above_diagonal_negative())
    
    def test_are_above_diagonal_negative_before_processing(self):
        """Тест проверки отрицательности элементов на диагонали и выше до обработки"""
        values = [[1, 2], [3, 4]]
        self.processor.create_matrix(2, values)
        # Не вызываем process_matrix()
        self.assertFalse(self.processor.are_above_diagonal_negative())
    
    def test_are_above_diagonal_negative_no_matrix(self):
        """Тест проверки отрицательности элементов на диагонали и выше когда матрица не создана"""
        self.assertTrue(self.processor.are_above_diagonal_negative())  # Должно возвращать True для пустой матрицы
    
    # Тесты экстремальных значений
    
    def test_extreme_values_min(self):
        """Тест с минимальными значениями"""
        values = [[1, 1], [1, 1]]
        self.processor.create_matrix(2, values)
        result = self.processor.process_matrix()
        self.assertTrue(result)
        self.assertTrue(self.processor.is_sorted_below_diagonal())
        self.assertTrue(self.processor.are_above_diagonal_negative())
    
    def test_extreme_values_max(self):
        """Тест с максимальными значениями"""
        values = [[100, 100], [100, 100]]
        self.processor.create_matrix(2, values)
        result = self.processor.process_matrix()
        self.assertTrue(result)
        self.assertTrue(self.processor.is_sorted_below_diagonal())
        self.assertTrue(self.processor.are_above_diagonal_negative())
    
    def test_extreme_values_all_same(self):
        """Тест с одинаковыми значениями"""
        values = [[50, 50, 50], [50, 50, 50], [50, 50, 50]]
        self.processor.create_matrix(3, values)
        result = self.processor.process_matrix()
        self.assertTrue(result)
        self.assertTrue(self.processor.is_sorted_below_diagonal())
        self.assertTrue(self.processor.are_above_diagonal_negative())
    
    # Тесты сброса
    
    def test_reset(self):
        """Тест сброса матрицы"""
        self.processor.create_matrix(3)
        self.processor.reset()
        self.assertIsNone(self.processor.get_matrix())
        self.assertIsNone(self.processor.get_original_matrix())
        self.assertEqual(self.processor.get_size(), 0)
    
    # Тесты оригинальной матрицы
    
    def test_original_matrix_preservation(self):
        """Тест сохранения оригинальной матрицы"""
        values = [[1, 2], [3, 4]]
        self.processor.create_matrix(2, values)
        original = self.processor.get_original_matrix()
        self.assertEqual(original, values)
        
        # Обрабатываем матрицу
        self.processor.process_matrix()
        
        # Оригинальная матрица должна остаться неизменной
        original_after = self.processor.get_original_matrix()
        self.assertEqual(original_after, values)
        
        # Обработанная матрица должна отличаться от оригинальной
        processed = self.processor.get_matrix()
        self.assertNotEqual(processed, values)
    
    # Интеграционные тесты
    
    def test_full_workflow_2x2(self):
        """Интеграционный тест полного рабочего процесса для матрицы 2x2"""
        # Создаем матрицу
        values = [[10, 20], [30, 40]]
        self.assertTrue(self.processor.create_matrix(2, values))
        
        # Проверяем исходное состояние
        self.assertEqual(self.processor.get_elements_below_diagonal(), [30])
        self.assertEqual(self.processor.get_elements_above_and_on_diagonal(), [10, 20, 40])
        self.assertFalse(self.processor.are_above_diagonal_negative())
        
        # Обрабатываем матрицу
        self.assertTrue(self.processor.process_matrix())
        
        # Проверяем результаты
        self.assertTrue(self.processor.is_sorted_below_diagonal())
        self.assertTrue(self.processor.are_above_diagonal_negative())
        
        # Проверяем, что оригинальная матрица сохранена
        self.assertEqual(self.processor.get_original_matrix(), values)
    
    def test_full_workflow_3x3(self):
        """Интеграционный тест полного рабочего процесса для матрицы 3x3"""
        # Создаем матрицу
        values = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.assertTrue(self.processor.create_matrix(3, values))
        
        # Проверяем исходное состояние
        self.assertEqual(self.processor.get_elements_below_diagonal(), [4, 7, 8])
        self.assertEqual(self.processor.get_elements_above_and_on_diagonal(), [1, 2, 3, 5, 6, 9])
        
        # Обрабатываем матрицу
        self.assertTrue(self.processor.process_matrix())
        
        # Проверяем результаты
        self.assertTrue(self.processor.is_sorted_below_diagonal())
        self.assertTrue(self.processor.are_above_diagonal_negative())
        
        # Проверяем конкретные изменения
        processed = self.processor.get_matrix()
        # Элементы на диагонали и выше должны быть отрицательными
        self.assertLess(processed[0][0], 0)  # -1
        self.assertLess(processed[0][1], 0)  # -2
        self.assertLess(processed[0][2], 0)  # -3
        self.assertLess(processed[1][1], 0)  # -5
        self.assertLess(processed[1][2], 0)  # -6
        self.assertLess(processed[2][2], 0)  # -9


class TestMatrixProcessorV2EdgeCases(unittest.TestCase):
    """
    Дополнительные тесты для граничных случаев
    """
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        self.processor = MatrixProcessorV2()
    
    def tearDown(self):
        """Очистка после каждого теста"""
        self.processor.reset()
    
    def test_matrix_with_zeros_after_processing(self):
        """Тест матрицы с нулями после обработки"""
        values = [[0, 0], [0, 0]]
        # Сначала создаем с корректными значениями
        self.processor.create_matrix(2, [[1, 1], [1, 1]])
        # Затем вручную устанавливаем нули
        self.processor.set_element(0, 0, 1)  # Это должно работать
        # Но нули не входят в допустимый диапазон [1, 100]
        result = self.processor.set_element(0, 0, 0)
        self.assertFalse(result)
    
    def test_large_matrix_processing_time(self):
        """Тест времени обработки большой матрицы (5x5)"""
        import time
        
        # Создаем матрицу 5x5 с корректными значениями в диапазоне [1, 100]
        values = [[(i * 5 + j) % 100 + 1 for j in range(5)] for i in range(5)]
        self.assertTrue(self.processor.create_matrix(5, values))
        
        start_time = time.time()
        result = self.processor.process_matrix()
        end_time = time.time()
        
        self.assertTrue(result)
        self.assertLess(end_time - start_time, 1.0)  # Должно выполняться менее чем за секунду
    
    def test_multiple_processing_calls(self):
        """Тест множественных вызовов обработки"""
        values = [[1, 2], [3, 4]]
        self.processor.create_matrix(2, values)
        
        # Первая обработка
        self.assertTrue(self.processor.process_matrix())
        first_result = self.processor.get_matrix()
        
        # Проверяем результат первой обработки
        self.assertTrue(self.processor.is_sorted_below_diagonal())
        self.assertTrue(self.processor.are_above_diagonal_negative())
        
        # Вторая обработка (не идемпотентна из-за умножения на -1)
        self.assertTrue(self.processor.process_matrix())
        second_result = self.processor.get_matrix()
        
        # Результаты должны отличаться (не идемпотентность)
        self.assertNotEqual(first_result, second_result)
        
        # После второй обработки элементы на диагонали и выше становятся положительными
        # (отрицательные числа умножаются на -1)
        self.assertTrue(self.processor.is_sorted_below_diagonal())
        self.assertFalse(self.processor.are_above_diagonal_negative())  # Теперь положительные


def run_tests():
    """
    Запуск всех тестов с подробным выводом
    """
    # Создаем test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Добавляем тесты
    suite.addTests(loader.loadTestsFromTestCase(TestMatrixProcessorV2))
    suite.addTests(loader.loadTestsFromTestCase(TestMatrixProcessorV2EdgeCases))
    
    # Запускаем тесты с подробным выводом
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == "__main__":
    print("ЗАПУСК СИСТЕМЫ МОДУЛЬНОГО ТЕСТИРОВАНИЯ")
    print("Практическая работа №6 - Вариант 7")
    print("=" * 60)
    
    result = run_tests()
    
    print("\n" + "=" * 60)
    print("ИТОГОВАЯ СВОДКА ТЕСТИРОВАНИЯ")
    print("=" * 60)
    print(f"Всего тестов: {result.testsRun}")
    print(f"Пройдено: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Провалено: {len(result.failures)}")
    print(f"Ошибок: {len(result.errors)}")
    
    if result.failures:
        print(f"\nПРОВАЛЕННЫЕ ТЕСТЫ ({len(result.failures)}):")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('AssertionError: ')[-1].split('\\n')[0]}")
    
    if result.errors:
        print(f"\nОШИБКИ ({len(result.errors)}):")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('\\n')[-2]}")
    
    success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun) * 100
    print(f"\nПроцент успешности: {success_rate:.1f}%")
    
    if success_rate == 100.0:
        print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
    else:
        print(f"\n⚠️  ТРЕБУЕТСЯ ИСПРАВЛЕНИЕ {len(result.failures) + len(result.errors)} ТЕСТОВ")
