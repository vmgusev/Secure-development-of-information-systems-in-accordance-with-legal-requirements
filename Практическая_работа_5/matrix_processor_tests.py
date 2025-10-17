#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Класс для юнит-тестирования MatrixProcessor
Практическая работа №5 - Вариант 7

Автор: Гусев В.М. КВМО-11-24
Дата: 2025
"""

from matrix_processor import MatrixProcessor


class MatrixProcessorTester:
    """
    Класс для тестирования MatrixProcessor без использования специализированных библиотек
    """
    
    def __init__(self):
        """Инициализация тестера"""
        self.passed_tests = 0
        self.failed_tests = 0
        self.test_results = []
    
    def run_test(self, test_name: str, test_function) -> bool:
        """
        Запуск одного теста
        
        Args:
            test_name: Название теста
            test_function: Функция теста
            
        Returns:
            bool: True если тест прошел успешно
        """
        try:
            result = test_function()
            if result:
                self.passed_tests += 1
                self.test_results.append(f"✓ {test_name}: ПРОЙДЕН")
                print(f"✓ {test_name}: ПРОЙДЕН")
                return True
            else:
                self.failed_tests += 1
                self.test_results.append(f"✗ {test_name}: ПРОВАЛЕН")
                print(f"✗ {test_name}: ПРОВАЛЕН")
                return False
        except Exception as e:
            self.failed_tests += 1
            self.test_results.append(f"✗ {test_name}: ОШИБКА - {str(e)}")
            print(f"✗ {test_name}: ОШИБКА - {str(e)}")
            return False
    
    def run_all_tests(self) -> None:
        """Запуск всех тестов"""
        print("Запуск тестирования MatrixProcessor")
        print("=" * 50)
        
        # Тесты создания матрицы
        self.run_test("test_create_matrix_valid_size_2", self.test_create_matrix_valid_size_2)
        self.run_test("test_create_matrix_valid_size_5", self.test_create_matrix_valid_size_5)
        self.run_test("test_create_matrix_invalid_size_1", self.test_create_matrix_invalid_size_1)
        self.run_test("test_create_matrix_invalid_size_6", self.test_create_matrix_invalid_size_6)
        self.run_test("test_create_matrix_invalid_size_negative", self.test_create_matrix_invalid_size_negative)
        self.run_test("test_create_matrix_invalid_size_float", self.test_create_matrix_invalid_size_float)
        
        # Тесты создания матрицы с пользовательскими значениями
        self.run_test("test_create_matrix_with_valid_values", self.test_create_matrix_with_valid_values)
        self.run_test("test_create_matrix_with_invalid_values_wrong_size", self.test_create_matrix_with_invalid_values_wrong_size)
        self.run_test("test_create_matrix_with_invalid_values_out_of_range", self.test_create_matrix_with_invalid_values_out_of_range)
        self.run_test("test_create_matrix_with_invalid_values_wrong_type", self.test_create_matrix_with_invalid_values_wrong_type)
        
        # Тесты получения элементов
        self.run_test("test_get_element_valid_coordinates", self.test_get_element_valid_coordinates)
        self.run_test("test_get_element_invalid_coordinates", self.test_get_element_invalid_coordinates)
        self.run_test("test_get_element_no_matrix", self.test_get_element_no_matrix)
        
        # Тесты установки элементов
        self.run_test("test_set_element_valid", self.test_set_element_valid)
        self.run_test("test_set_element_invalid_coordinates", self.test_set_element_invalid_coordinates)
        self.run_test("test_set_element_invalid_value", self.test_set_element_invalid_value)
        self.run_test("test_set_element_no_matrix", self.test_set_element_no_matrix)
        
        # Тесты сортировки
        self.run_test("test_sort_below_diagonal_2x2", self.test_sort_below_diagonal_2x2)
        self.run_test("test_sort_below_diagonal_3x3", self.test_sort_below_diagonal_3x3)
        self.run_test("test_sort_below_diagonal_4x4", self.test_sort_below_diagonal_4x4)
        self.run_test("test_sort_below_diagonal_5x5", self.test_sort_below_diagonal_5x5)
        self.run_test("test_sort_below_diagonal_no_matrix", self.test_sort_below_diagonal_no_matrix)
        
        # Тесты получения элементов ниже диагонали
        self.run_test("test_get_elements_below_diagonal_2x2", self.test_get_elements_below_diagonal_2x2)
        self.run_test("test_get_elements_below_diagonal_3x3", self.test_get_elements_below_diagonal_3x3)
        self.run_test("test_get_elements_below_diagonal_no_matrix", self.test_get_elements_below_diagonal_no_matrix)
        
        # Тесты проверки сортировки
        self.run_test("test_is_sorted_below_diagonal_sorted", self.test_is_sorted_below_diagonal_sorted)
        self.run_test("test_is_sorted_below_diagonal_not_sorted", self.test_is_sorted_below_diagonal_not_sorted)
        self.run_test("test_is_sorted_below_diagonal_no_matrix", self.test_is_sorted_below_diagonal_no_matrix)
        
        # Тесты экстремальных значений
        self.run_test("test_extreme_values_min", self.test_extreme_values_min)
        self.run_test("test_extreme_values_max", self.test_extreme_values_max)
        self.run_test("test_extreme_values_all_same", self.test_extreme_values_all_same)
        
        # Тесты сброса
        self.run_test("test_reset", self.test_reset)
        
        # Вывод результатов
        self.print_summary()
    
    def print_summary(self) -> None:
        """Вывод сводки результатов тестирования"""
        print("\n" + "=" * 50)
        print("СВОДКА РЕЗУЛЬТАТОВ ТЕСТИРОВАНИЯ")
        print("=" * 50)
        print(f"Всего тестов: {self.passed_tests + self.failed_tests}")
        print(f"Пройдено: {self.passed_tests}")
        print(f"Провалено: {self.failed_tests}")
        print(f"Процент успешности: {(self.passed_tests / (self.passed_tests + self.failed_tests) * 100):.1f}%")
        
        if self.failed_tests > 0:
            print("\nПРОВАЛЕННЫЕ ТЕСТЫ:")
            for result in self.test_results:
                if result.startswith("✗"):
                    print(f"  {result}")
    
    # Позитивные тесты
    
    def test_create_matrix_valid_size_2(self) -> bool:
        """Тест создания матрицы размера 2x2"""
        processor = MatrixProcessor()
        return processor.create_matrix(2)
    
    def test_create_matrix_valid_size_5(self) -> bool:
        """Тест создания матрицы размера 5x5"""
        processor = MatrixProcessor()
        return processor.create_matrix(5)
    
    def test_create_matrix_with_valid_values(self) -> bool:
        """Тест создания матрицы с корректными пользовательскими значениями"""
        processor = MatrixProcessor()
        values = [[1, 2], [3, 4]]
        return processor.create_matrix(2, values)
    
    def test_get_element_valid_coordinates(self) -> bool:
        """Тест получения элемента по корректным координатам"""
        processor = MatrixProcessor()
        processor.create_matrix(3)
        element = processor.get_element(1, 1)
        return element is not None and isinstance(element, int)
    
    def test_set_element_valid(self) -> bool:
        """Тест установки корректного значения элемента"""
        processor = MatrixProcessor()
        processor.create_matrix(2)
        return processor.set_element(0, 1, 50)
    
    def test_sort_below_diagonal_2x2(self) -> bool:
        """Тест сортировки матрицы 2x2"""
        processor = MatrixProcessor()
        values = [[10, 20], [30, 40]]
        processor.create_matrix(2, values)
        result = processor.sort_below_diagonal()
        return result and processor.is_sorted_below_diagonal()
    
    def test_sort_below_diagonal_3x3(self) -> bool:
        """Тест сортировки матрицы 3x3"""
        processor = MatrixProcessor()
        values = [[10, 20, 30], [40, 50, 60], [70, 80, 90]]
        processor.create_matrix(3, values)
        result = processor.sort_below_diagonal()
        return result and processor.is_sorted_below_diagonal()
    
    def test_sort_below_diagonal_4x4(self) -> bool:
        """Тест сортировки матрицы 4x4"""
        processor = MatrixProcessor()
        values = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
        processor.create_matrix(4, values)
        result = processor.sort_below_diagonal()
        return result and processor.is_sorted_below_diagonal()
    
    def test_sort_below_diagonal_5x5(self) -> bool:
        """Тест сортировки матрицы 5x5"""
        processor = MatrixProcessor()
        values = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15], 
                 [16, 17, 18, 19, 20], [21, 22, 23, 24, 25]]
        processor.create_matrix(5, values)
        result = processor.sort_below_diagonal()
        return result and processor.is_sorted_below_diagonal()
    
    def test_get_elements_below_diagonal_2x2(self) -> bool:
        """Тест получения элементов ниже диагонали для матрицы 2x2"""
        processor = MatrixProcessor()
        values = [[1, 2], [3, 4]]
        processor.create_matrix(2, values)
        elements = processor.get_elements_below_diagonal()
        return elements == [3]
    
    def test_get_elements_below_diagonal_3x3(self) -> bool:
        """Тест получения элементов ниже диагонали для матрицы 3x3"""
        processor = MatrixProcessor()
        values = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        processor.create_matrix(3, values)
        elements = processor.get_elements_below_diagonal()
        return elements == [4, 7, 8]
    
    def test_is_sorted_below_diagonal_sorted(self) -> bool:
        """Тест проверки сортировки для уже отсортированной матрицы"""
        processor = MatrixProcessor()
        values = [[1, 2], [3, 4]]
        processor.create_matrix(2, values)
        processor.sort_below_diagonal()
        return processor.is_sorted_below_diagonal()
    
    def test_extreme_values_min(self) -> bool:
        """Тест с минимальными значениями"""
        processor = MatrixProcessor()
        values = [[1, 1], [1, 1]]
        processor.create_matrix(2, values)
        return processor.sort_below_diagonal() and processor.is_sorted_below_diagonal()
    
    def test_extreme_values_max(self) -> bool:
        """Тест с максимальными значениями"""
        processor = MatrixProcessor()
        values = [[100, 100], [100, 100]]
        processor.create_matrix(2, values)
        return processor.sort_below_diagonal() and processor.is_sorted_below_diagonal()
    
    def test_extreme_values_all_same(self) -> bool:
        """Тест с одинаковыми значениями"""
        processor = MatrixProcessor()
        values = [[50, 50, 50], [50, 50, 50], [50, 50, 50]]
        processor.create_matrix(3, values)
        return processor.sort_below_diagonal() and processor.is_sorted_below_diagonal()
    
    def test_reset(self) -> bool:
        """Тест сброса матрицы"""
        processor = MatrixProcessor()
        processor.create_matrix(3)
        processor.reset()
        return processor.get_matrix() is None and processor.get_size() == 0
    
    # Негативные тесты
    
    def test_create_matrix_invalid_size_1(self) -> bool:
        """Тест создания матрицы недопустимого размера 1"""
        processor = MatrixProcessor()
        return not processor.create_matrix(1)
    
    def test_create_matrix_invalid_size_6(self) -> bool:
        """Тест создания матрицы недопустимого размера 6"""
        processor = MatrixProcessor()
        return not processor.create_matrix(6)
    
    def test_create_matrix_invalid_size_negative(self) -> bool:
        """Тест создания матрицы с отрицательным размером"""
        processor = MatrixProcessor()
        return not processor.create_matrix(-2)
    
    def test_create_matrix_invalid_size_float(self) -> bool:
        """Тест создания матрицы с размером типа float"""
        processor = MatrixProcessor()
        return not processor.create_matrix(3.5)
    
    def test_create_matrix_with_invalid_values_wrong_size(self) -> bool:
        """Тест создания матрицы с неверным размером значений"""
        processor = MatrixProcessor()
        values = [[1, 2, 3], [4, 5]]  # Неправильный размер
        return not processor.create_matrix(2, values)
    
    def test_create_matrix_with_invalid_values_out_of_range(self) -> bool:
        """Тест создания матрицы со значениями вне диапазона"""
        processor = MatrixProcessor()
        values = [[1, 2], [101, 4]]  # 101 вне диапазона [1, 100]
        return not processor.create_matrix(2, values)
    
    def test_create_matrix_with_invalid_values_wrong_type(self) -> bool:
        """Тест создания матрицы с неверным типом значений"""
        processor = MatrixProcessor()
        values = [[1, 2], ["3", 4]]  # "3" не является int
        return not processor.create_matrix(2, values)
    
    def test_get_element_invalid_coordinates(self) -> bool:
        """Тест получения элемента по неверным координатам"""
        processor = MatrixProcessor()
        processor.create_matrix(2)
        element = processor.get_element(5, 5)  # Координаты вне матрицы
        return element is None
    
    def test_get_element_no_matrix(self) -> bool:
        """Тест получения элемента когда матрица не создана"""
        processor = MatrixProcessor()
        element = processor.get_element(0, 0)
        return element is None
    
    def test_set_element_invalid_coordinates(self) -> bool:
        """Тест установки элемента по неверным координатам"""
        processor = MatrixProcessor()
        processor.create_matrix(2)
        return not processor.set_element(5, 5, 50)
    
    def test_set_element_invalid_value(self) -> bool:
        """Тест установки неверного значения элемента"""
        processor = MatrixProcessor()
        processor.create_matrix(2)
        return not processor.set_element(0, 0, 101)  # Значение вне диапазона
    
    def test_set_element_no_matrix(self) -> bool:
        """Тест установки элемента когда матрица не создана"""
        processor = MatrixProcessor()
        return not processor.set_element(0, 0, 50)
    
    def test_sort_below_diagonal_no_matrix(self) -> bool:
        """Тест сортировки когда матрица не создана"""
        processor = MatrixProcessor()
        return not processor.sort_below_diagonal()
    
    def test_get_elements_below_diagonal_no_matrix(self) -> bool:
        """Тест получения элементов ниже диагонали когда матрица не создана"""
        processor = MatrixProcessor()
        elements = processor.get_elements_below_diagonal()
        return elements == []
    
    def test_is_sorted_below_diagonal_not_sorted(self) -> bool:
        """Тест проверки сортировки для неотсортированной матрицы"""
        processor = MatrixProcessor()
        values = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]  # Элементы ниже диагонали: [4, 7, 8] - не отсортированы по убыванию
        processor.create_matrix(3, values)
        # Не вызываем sort_below_diagonal()
        return not processor.is_sorted_below_diagonal()
    
    def test_is_sorted_below_diagonal_no_matrix(self) -> bool:
        """Тест проверки сортировки когда матрица не создана"""
        processor = MatrixProcessor()
        return processor.is_sorted_below_diagonal()  # Должно возвращать True для пустой матрицы


def main():
    """Основная функция для запуска тестов"""
    tester = MatrixProcessorTester()
    tester.run_all_tests()


if __name__ == "__main__":
    main()
