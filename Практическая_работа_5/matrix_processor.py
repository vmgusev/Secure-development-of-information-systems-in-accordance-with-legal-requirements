#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Программа для работы с квадратными матрицами
Практическая работа №5 - Вариант 7

Автор: Гусев В.М. КВМО-11-24
Дата: 2025
"""

import random
from typing import List, Optional, Tuple


class MatrixProcessor:
    """
    Класс для создания и обработки квадратных матриц
    
    Функциональность:
    - Создание квадратной матрицы размера MxM (M ∈ [2,5])
    - Заполнение матрицы целыми числами из диапазона [1, 100]
    - Сортировка элементов ниже главной диагонали по убыванию
    """
    
    def __init__(self):
        """Инициализация процессора матриц"""
        self.matrix: Optional[List[List[int]]] = None
        self.size: int = 0
    
    def create_matrix(self, size: int, values: Optional[List[List[int]]] = None) -> bool:
        """
        Создание квадратной матрицы заданного размера
        
        Args:
            size: Размер матрицы (должен быть в диапазоне [2, 5])
            values: Опциональные значения для заполнения матрицы
            
        Returns:
            bool: True если матрица создана успешно, False в противном случае
        """
        if not self._validate_size(size):
            return False
        
        self.size = size
        self.matrix = []
        
        if values is not None:
            # Проверяем, что переданные значения корректны
            if not self._validate_values(values, size):
                return False
            self.matrix = [row[:] for row in values]  # Копируем значения
        else:
            # Заполняем случайными значениями
            self._fill_random_values()
        
        return True
    
    def _validate_size(self, size: int) -> bool:
        """
        Проверка корректности размера матрицы
        
        Args:
            size: Размер матрицы
            
        Returns:
            bool: True если размер корректный
        """
        return isinstance(size, int) and 2 <= size <= 5
    
    def _validate_values(self, values: List[List[int]], size: int) -> bool:
        """
        Проверка корректности переданных значений
        
        Args:
            values: Список списков с значениями
            size: Ожидаемый размер матрицы
            
        Returns:
            bool: True если значения корректны
        """
        if not isinstance(values, list) or len(values) != size:
            return False
        
        for row in values:
            if not isinstance(row, list) or len(row) != size:
                return False
            for value in row:
                if not isinstance(value, int) or not (1 <= value <= 100):
                    return False
        
        return True
    
    def _fill_random_values(self) -> None:
        """Заполнение матрицы случайными значениями"""
        self.matrix = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                row.append(random.randint(1, 100))
            self.matrix.append(row)
    
    def sort_below_diagonal(self) -> bool:
        """
        Сортировка элементов ниже главной диагонали по убыванию
        
        Returns:
            bool: True если сортировка выполнена успешно
        """
        if self.matrix is None:
            return False
        
        # Собираем все элементы ниже главной диагонали
        below_diagonal = []
        positions = []
        
        for i in range(self.size):
            for j in range(self.size):
                if i > j:  # Элементы ниже главной диагонали
                    below_diagonal.append(self.matrix[i][j])
                    positions.append((i, j))
        
        # Сортируем по убыванию
        below_diagonal.sort(reverse=True)
        
        # Заменяем элементы в матрице
        for k, (i, j) in enumerate(positions):
            self.matrix[i][j] = below_diagonal[k]
        
        return True
    
    def get_matrix(self) -> Optional[List[List[int]]]:
        """
        Получение текущей матрицы
        
        Returns:
            List[List[int]]: Копия матрицы или None если матрица не создана
        """
        if self.matrix is None:
            return None
        return [row[:] for row in self.matrix]
    
    def get_size(self) -> int:
        """
        Получение размера матрицы
        
        Returns:
            int: Размер матрицы
        """
        return self.size
    
    def get_element(self, row: int, col: int) -> Optional[int]:
        """
        Получение элемента матрицы по координатам
        
        Args:
            row: Номер строки (начиная с 0)
            col: Номер столбца (начиная с 0)
            
        Returns:
            int: Значение элемента или None если координаты некорректны
        """
        if self.matrix is None:
            return None
        
        if not (0 <= row < self.size and 0 <= col < self.size):
            return None
        
        return self.matrix[row][col]
    
    def set_element(self, row: int, col: int, value: int) -> bool:
        """
        Установка значения элемента матрицы
        
        Args:
            row: Номер строки (начиная с 0)
            col: Номер столбца (начиная с 0)
            value: Новое значение элемента
            
        Returns:
            bool: True если значение установлено успешно
        """
        if self.matrix is None:
            return False
        
        if not (0 <= row < self.size and 0 <= col < self.size):
            return False
        
        if not (isinstance(value, int) and 1 <= value <= 100):
            return False
        
        self.matrix[row][col] = value
        return True
    
    def get_elements_below_diagonal(self) -> List[int]:
        """
        Получение всех элементов ниже главной диагонали
        
        Returns:
            List[int]: Список элементов ниже главной диагонали
        """
        if self.matrix is None:
            return []
        
        elements = []
        for i in range(self.size):
            for j in range(self.size):
                if i > j:
                    elements.append(self.matrix[i][j])
        
        return elements
    
    def is_sorted_below_diagonal(self) -> bool:
        """
        Проверка, отсортированы ли элементы ниже главной диагонали по убыванию
        
        Returns:
            bool: True если элементы отсортированы по убыванию
        """
        elements = self.get_elements_below_diagonal()
        
        if len(elements) <= 1:
            return True
        
        for i in range(len(elements) - 1):
            if elements[i] < elements[i + 1]:
                return False
        
        return True
    
    def display_matrix(self) -> str:
        """
        Отображение матрицы в виде строки
        
        Returns:
            str: Строковое представление матрицы
        """
        if self.matrix is None:
            return "Матрица не создана"
        
        result = []
        for row in self.matrix:
            result.append(" ".join(f"{value:3d}" for value in row))
        
        return "\n".join(result)
    
    def reset(self) -> None:
        """Сброс матрицы"""
        self.matrix = None
        self.size = 0


def main():
    """
    Основная функция для демонстрации работы класса
    """
    print("Программа для работы с квадратными матрицами")
    print("=" * 50)
    
    processor = MatrixProcessor()
    
    # Демонстрация работы с матрицей 3x3
    print("\n1. Создание матрицы 3x3 со случайными значениями:")
    if processor.create_matrix(3):
        print(processor.display_matrix())
        
        print("\n2. Элементы ниже главной диагонали:")
        elements = processor.get_elements_below_diagonal()
        print(f"До сортировки: {elements}")
        
        print("\n3. Сортировка элементов ниже главной диагонали по убыванию:")
        if processor.sort_below_diagonal():
            print(processor.display_matrix())
            print(f"После сортировки: {processor.get_elements_below_diagonal()}")
            print(f"Отсортированы по убыванию: {processor.is_sorted_below_diagonal()}")
    
    # Демонстрация работы с пользовательскими значениями
    print("\n" + "=" * 50)
    print("4. Создание матрицы 4x4 с пользовательскими значениями:")
    user_values = [
        [10, 20, 30, 40],
        [50, 60, 70, 80],
        [90, 15, 25, 35],
        [45, 55, 65, 75]
    ]
    
    if processor.create_matrix(4, user_values):
        print(processor.display_matrix())
        print(f"Элементы ниже диагонали: {processor.get_elements_below_diagonal()}")
        
        processor.sort_below_diagonal()
        print("\nПосле сортировки:")
        print(processor.display_matrix())
        print(f"Элементы ниже диагонали: {processor.get_elements_below_diagonal()}")


if __name__ == "__main__":
    main()
