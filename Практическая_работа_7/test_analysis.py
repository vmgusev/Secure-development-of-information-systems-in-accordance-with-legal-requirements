#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Анализ классов эквивалентности и граничных условий для тестирования калькулятора
Практическая работа №7 - Вариант 7

Автор: Гусев В.М. КВМО-11-24
Дата: 2025
"""

from typing import List, Tuple, Dict, Any
import math


class TestCaseAnalyzer:
    """
    Класс для анализа тестовых случаев на основе классов эквивалентности
    и граничных условий
    """
    
    def __init__(self):
        """Инициализация анализатора"""
        self.equivalence_classes = {}
        self.boundary_conditions = {}
        self.test_cases = []
    
    def analyze_arithmetic_operations(self) -> Dict[str, Any]:
        """
        Анализ арифметических операций калькулятора
        
        Returns:
            Dict: Результаты анализа
        """
        analysis = {
            "addition": self._analyze_addition(),
            "subtraction": self._analyze_subtraction(),
            "multiplication": self._analyze_multiplication(),
            "division": self._analyze_division(),
            "boundary_conditions": self._analyze_boundary_conditions()
        }
        
        return analysis
    
    def _analyze_addition(self) -> Dict[str, Any]:
        """Анализ операции сложения"""
        return {
            "equivalence_classes": {
                "positive_positive": {
                    "description": "Сложение двух положительных чисел",
                    "examples": ["2+3", "10+5", "100+200"],
                    "expected_behavior": "Положительный результат"
                },
                "positive_zero": {
                    "description": "Сложение положительного числа с нулем",
                    "examples": ["5+0", "100+0"],
                    "expected_behavior": "Результат равен первому числу"
                },
                "zero_positive": {
                    "description": "Сложение нуля с положительным числом",
                    "examples": ["0+5", "0+100"],
                    "expected_behavior": "Результат равен второму числу"
                },
                "negative_negative": {
                    "description": "Сложение двух отрицательных чисел",
                    "examples": ["(-2)+(-3)", "(-10)+(-5)"],
                    "expected_behavior": "Отрицательный результат"
                },
                "positive_negative": {
                    "description": "Сложение положительного и отрицательного числа",
                    "examples": ["5+(-3)", "10+(-5)"],
                    "expected_behavior": "Результат зависит от абсолютных значений"
                },
                "decimal_numbers": {
                    "description": "Сложение десятичных чисел",
                    "examples": ["2.5+3.7", "1.1+2.2"],
                    "expected_behavior": "Десятичный результат"
                }
            },
            "boundary_conditions": {
                "max_values": {
                    "description": "Максимальные значения",
                    "test_cases": ["999999+1", "999999+999999"],
                    "expected_behavior": "Корректная обработка больших чисел"
                },
                "min_values": {
                    "description": "Минимальные значения",
                    "test_cases": ["1+1", "0+0"],
                    "expected_behavior": "Корректная обработка малых чисел"
                },
                "precision_limits": {
                    "description": "Границы точности",
                    "test_cases": ["0.1+0.2", "0.0001+0.0001"],
                    "expected_behavior": "Корректная обработка точности"
                }
            }
        }
    
    def _analyze_subtraction(self) -> Dict[str, Any]:
        """Анализ операции вычитания"""
        return {
            "equivalence_classes": {
                "positive_positive": {
                    "description": "Вычитание положительного из положительного",
                    "examples": ["5-3", "10-5", "100-50"],
                    "expected_behavior": "Положительный результат (если уменьшаемое больше)"
                },
                "positive_negative": {
                    "description": "Вычитание отрицательного из положительного",
                    "examples": ["5-(-3)", "10-(-5)"],
                    "expected_behavior": "Эквивалентно сложению"
                },
                "negative_positive": {
                    "description": "Вычитание положительного из отрицательного",
                    "examples": ["(-5)-3", "(-10)-5"],
                    "expected_behavior": "Отрицательный результат"
                },
                "zero_subtraction": {
                    "description": "Вычитание из нуля или нуля",
                    "examples": ["0-5", "5-0", "0-0"],
                    "expected_behavior": "Корректная обработка нуля"
                },
                "decimal_subtraction": {
                    "description": "Вычитание десятичных чисел",
                    "examples": ["5.5-2.3", "1.1-0.1"],
                    "expected_behavior": "Десятичный результат"
                }
            },
            "boundary_conditions": {
                "result_zero": {
                    "description": "Результат равен нулю",
                    "test_cases": ["5-5", "0-0"],
                    "expected_behavior": "Корректное отображение нуля"
                },
                "negative_result": {
                    "description": "Отрицательный результат",
                    "test_cases": ["3-5", "0-1"],
                    "expected_behavior": "Корректное отображение отрицательного числа"
                }
            }
        }
    
    def _analyze_multiplication(self) -> Dict[str, Any]:
        """Анализ операции умножения"""
        return {
            "equivalence_classes": {
                "positive_positive": {
                    "description": "Умножение двух положительных чисел",
                    "examples": ["3*4", "10*5", "100*2"],
                    "expected_behavior": "Положительный результат"
                },
                "positive_zero": {
                    "description": "Умножение на ноль",
                    "examples": ["5*0", "100*0"],
                    "expected_behavior": "Результат равен нулю"
                },
                "positive_one": {
                    "description": "Умножение на единицу",
                    "examples": ["5*1", "100*1"],
                    "expected_behavior": "Результат равен первому числу"
                },
                "negative_negative": {
                    "description": "Умножение двух отрицательных чисел",
                    "examples": ["(-3)*(-4)", "(-10)*(-5)"],
                    "expected_behavior": "Положительный результат"
                },
                "positive_negative": {
                    "description": "Умножение положительного на отрицательное",
                    "examples": ["3*(-4)", "10*(-5)"],
                    "expected_behavior": "Отрицательный результат"
                },
                "decimal_multiplication": {
                    "description": "Умножение десятичных чисел",
                    "examples": ["2.5*4", "1.1*2.2"],
                    "expected_behavior": "Десятичный результат"
                }
            },
            "boundary_conditions": {
                "large_numbers": {
                    "description": "Умножение больших чисел",
                    "test_cases": ["999*999", "1000*1000"],
                    "expected_behavior": "Корректная обработка переполнения"
                },
                "small_numbers": {
                    "description": "Умножение малых чисел",
                    "test_cases": ["0.1*0.1", "0.001*0.001"],
                    "expected_behavior": "Корректная обработка точности"
                }
            }
        }
    
    def _analyze_division(self) -> Dict[str, Any]:
        """Анализ операции деления"""
        return {
            "equivalence_classes": {
                "positive_positive": {
                    "description": "Деление положительного на положительное",
                    "examples": ["8/2", "10/5", "100/25"],
                    "expected_behavior": "Положительный результат"
                },
                "division_by_one": {
                    "description": "Деление на единицу",
                    "examples": ["5/1", "100/1"],
                    "expected_behavior": "Результат равен делимому"
                },
                "division_by_zero": {
                    "description": "Деление на ноль",
                    "examples": ["5/0", "100/0"],
                    "expected_behavior": "Ошибка или бесконечность"
                },
                "zero_division": {
                    "description": "Деление нуля на число",
                    "examples": ["0/5", "0/100"],
                    "expected_behavior": "Результат равен нулю"
                },
                "negative_division": {
                    "description": "Деление с отрицательными числами",
                    "examples": ["(-8)/(-2)", "8/(-2)", "(-8)/2"],
                    "expected_behavior": "Результат зависит от знаков"
                },
                "decimal_division": {
                    "description": "Деление десятичных чисел",
                    "examples": ["7.5/2.5", "1.1/0.1"],
                    "expected_behavior": "Десятичный результат"
                }
            },
            "boundary_conditions": {
                "exact_division": {
                    "description": "Точное деление",
                    "test_cases": ["8/2", "10/5"],
                    "expected_behavior": "Целочисленный результат"
                },
                "repeating_decimals": {
                    "description": "Бесконечные десятичные дроби",
                    "test_cases": ["1/3", "2/3"],
                    "expected_behavior": "Корректное округление"
                },
                "very_small_divisor": {
                    "description": "Деление на очень маленькое число",
                    "test_cases": ["1/0.001", "1/0.0001"],
                    "expected_behavior": "Корректная обработка больших результатов"
                }
            }
        }
    
    def _analyze_boundary_conditions(self) -> Dict[str, Any]:
        """Анализ общих граничных условий"""
        return {
            "input_limits": {
                "description": "Границы входных данных",
                "test_cases": [
                    "999999+1",  # Максимальные числа
                    "0+0",       # Минимальные числа
                    "0.0001+0.0001",  # Очень малые числа
                    "999.999+0.001"   # Смешанная точность
                ]
            },
            "precision_limits": {
                "description": "Границы точности вычислений",
                "test_cases": [
                    "0.1+0.2",      # Проблема точности с плавающей точкой
                    "1/3",          # Бесконечная десятичная дробь
                    "0.0001*0.0001" # Очень малые произведения
                ]
            },
            "display_limits": {
                "description": "Границы отображения результатов",
                "test_cases": [
                    "999999*999999",  # Очень большие результаты
                    "0.0000001",      # Очень малые результаты
                    "1/0"             # Деление на ноль
                ]
            }
        }
    
    def generate_test_cases(self) -> List[Dict[str, Any]]:
        """
        Генерация тестовых случаев на основе анализа
        
        Returns:
            List: Список тестовых случаев
        """
        test_cases = []
        
        # Тесты сложения
        test_cases.extend([
            {"operation": "addition", "expression": "2+3", "expected": 5.0, "class": "positive_positive"},
            {"operation": "addition", "expression": "5+0", "expected": 5.0, "class": "positive_zero"},
            {"operation": "addition", "expression": "0+5", "expected": 5.0, "class": "zero_positive"},
            {"operation": "addition", "expression": "(-2)+(-3)", "expected": -5.0, "class": "negative_negative"},
            {"operation": "addition", "expression": "2.5+3.7", "expected": 6.2, "class": "decimal_numbers"},
            {"operation": "addition", "expression": "999999+1", "expected": 1000000.0, "class": "boundary_max"},
        ])
        
        # Тесты вычитания
        test_cases.extend([
            {"operation": "subtraction", "expression": "5-3", "expected": 2.0, "class": "positive_positive"},
            {"operation": "subtraction", "expression": "5-0", "expected": 5.0, "class": "zero_subtraction"},
            {"operation": "subtraction", "expression": "0-5", "expected": -5.0, "class": "zero_subtraction"},
            {"operation": "subtraction", "expression": "5.5-2.3", "expected": 3.2, "class": "decimal_subtraction"},
            {"operation": "subtraction", "expression": "5-5", "expected": 0.0, "class": "boundary_zero"},
        ])
        
        # Тесты умножения
        test_cases.extend([
            {"operation": "multiplication", "expression": "3*4", "expected": 12.0, "class": "positive_positive"},
            {"operation": "multiplication", "expression": "5*0", "expected": 0.0, "class": "positive_zero"},
            {"operation": "multiplication", "expression": "5*1", "expected": 5.0, "class": "positive_one"},
            {"operation": "multiplication", "expression": "(-3)*(-4)", "expected": 12.0, "class": "negative_negative"},
            {"operation": "multiplication", "expression": "2.5*4", "expected": 10.0, "class": "decimal_multiplication"},
        ])
        
        # Тесты деления
        test_cases.extend([
            {"operation": "division", "expression": "8/2", "expected": 4.0, "class": "positive_positive"},
            {"operation": "division", "expression": "5/1", "expected": 5.0, "class": "division_by_one"},
            {"operation": "division", "expression": "0/5", "expected": 0.0, "class": "zero_division"},
            {"operation": "division", "expression": "7.5/2.5", "expected": 3.0, "class": "decimal_division"},
            {"operation": "division", "expression": "1/0.001", "expected": 1000.0, "class": "boundary_small_divisor"},
        ])
        
        return test_cases
    
    def print_analysis_report(self) -> None:
        """Вывод отчета анализа"""
        print("АНАЛИЗ КЛАССОВ ЭКВИВАЛЕНТНОСТИ И ГРАНИЧНЫХ УСЛОВИЙ")
        print("Практическая работа №7 - Вариант 7")
        print("=" * 70)
        
        analysis = self.analyze_arithmetic_operations()
        
        for operation, data in analysis.items():
            if operation == "boundary_conditions":
                continue
                
            print(f"\n{operation.upper()}")
            print("-" * 50)
            
            if "equivalence_classes" in data:
                print("КЛАССЫ ЭКВИВАЛЕНТНОСТИ:")
                for class_name, class_data in data["equivalence_classes"].items():
                    print(f"  • {class_data['description']}")
                    print(f"    Примеры: {', '.join(class_data['examples'])}")
                    print(f"    Ожидаемое поведение: {class_data['expected_behavior']}")
                    print()
            
            if "boundary_conditions" in data:
                print("ГРАНИЧНЫЕ УСЛОВИЯ:")
                for condition_name, condition_data in data["boundary_conditions"].items():
                    print(f"  • {condition_data['description']}")
                    print(f"    Тестовые случаи: {', '.join(condition_data['test_cases'])}")
                    print(f"    Ожидаемое поведение: {condition_data['expected_behavior']}")
                    print()
        
        # Общие граничные условия
        print("ОБЩИЕ ГРАНИЧНЫЕ УСЛОВИЯ")
        print("-" * 50)
        for condition_name, condition_data in analysis["boundary_conditions"].items():
            print(f"  • {condition_data['description']}")
            print(f"    Тестовые случаи: {', '.join(condition_data['test_cases'])}")
            print()
        
        # Генерация тестовых случаев
        print("СГЕНЕРИРОВАННЫЕ ТЕСТОВЫЕ СЛУЧАИ")
        print("-" * 50)
        test_cases = self.generate_test_cases()
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"{i:2d}. {test_case['operation']}: {test_case['expression']} = {test_case['expected']} ({test_case['class']})")
        
        print(f"\nВсего сгенерировано тестовых случаев: {len(test_cases)}")


def main():
    """Основная функция для запуска анализа"""
    analyzer = TestCaseAnalyzer()
    analyzer.print_analysis_report()


if __name__ == "__main__":
    main()
