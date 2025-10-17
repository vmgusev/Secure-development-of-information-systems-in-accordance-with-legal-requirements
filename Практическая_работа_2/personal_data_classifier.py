#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Программа для классификации согласий на обработку персональных данных
Практическая работа №2 - Вариант 7

Автор: Гусев В.М. КВМО-11-24
Дата: 2025
"""

import os
import re
import shutil
from pathlib import Path
from typing import List, Dict, Tuple, Optional

class PersonalDataClassifier:
    """
    Класс для анализа и классификации согласий на обработку персональных данных
    согласно требованиям ФЗ-152 "О персональных данных"
    """
    
    def __init__(self, input_dir: str, output_dir: str):
        """
        Инициализация классификатора
        
        Args:
            input_dir: Путь к папке с исходными файлами
            output_dir: Путь к папке для результатов
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.correct_dir = self.output_dir / "correct_agreements"
        self.incorrect_dir = self.output_dir / "incorrect_agreements"
        
        # Создаем выходные папки
        self.correct_dir.mkdir(parents=True, exist_ok=True)
        self.incorrect_dir.mkdir(parents=True, exist_ok=True)
        
        # Счетчики
        self.correct_count = 0
        self.incorrect_count = 0
        self.errors_log = []
        
        # Обязательные поля согласно ФЗ-152
        self.required_fields = {
            'subject_name': r'Я,\s+([А-Яа-яёЁ\s]+),\s+паспорт',
            'subject_address': r'зарегистрированный по адресу:\s*([^,\n]+)',
            'subject_passport': r'паспорт:\s*(\d+\s+\d+\s+\d+)',
            'passport_issued': r'выдан\s+(\d{2}\.\d{2}\.\d{4}г\.)',
            'passport_authority': r'ГУ МВД России по г\.\s+([^,]+)',
            'operator_name': r'даю согласие на обработку персональных данных\s+([^,\n]+)',
            'operator_address': r'зарегистрированному по адресу:\s*([^,\n]+)',
            'purpose': r'Целью сбора и обработки персональных данных является\s+([^,\n]+)',
            'data_list': r'В перечень персональных данных, подлежащих обработке, входят:\s*([^,\n]+)',
            'actions': r'Обработка персональных данных подразумевает выполнение следующих операций:\s*([^,\n]+)',
            'term': r'Согласие на обработку персональных данных действует\s+([^,\n]+)',
            'withdrawal': r'Согласие может быть отозвано субъектом персональных данных\s+([^,\n]+)',
            'signature': r'Подпись субъекта персональных данных\s+([^,\n]+)'
        }
    
    def read_file_with_encoding(self, file_path: Path) -> Optional[str]:
        """
        Читает файл с правильной кодировкой
        
        Args:
            file_path: Путь к файлу
            
        Returns:
            Содержимое файла или None при ошибке
        """
        encodings = ['utf-8', 'windows-1251', 'cp1251', 'latin1']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
        
        # Если не удалось прочитать с обычными кодировками, пробуем через iconv
        try:
            import subprocess
            result = subprocess.run(
                ['iconv', '-f', 'windows-1251', '-t', 'utf-8', str(file_path)],
                capture_output=True, text=True, check=True
            )
            return result.stdout
        except:
            return None
    
    def validate_agreement(self, content: str, filename: str) -> Tuple[bool, List[str]]:
        """
        Проверяет согласие на соответствие требованиям ФЗ-152
        
        Args:
            content: Содержимое файла
            filename: Имя файла для логирования
            
        Returns:
            Tuple[bool, List[str]]: (валидно ли согласие, список ошибок)
        """
        errors = []
        
        # Проверяем каждое обязательное поле
        for field_name, pattern in self.required_fields.items():
            match = re.search(pattern, content, re.IGNORECASE | re.MULTILINE)
            
            if not match:
                errors.append(f"Отсутствует поле: {field_name}")
            else:
                # Дополнительные проверки для критичных полей
                if field_name == 'operator_name':
                    operator_text = match.group(1).strip()
                    if not operator_text or operator_text.isspace():
                        errors.append(f"Пустое поле оператора: {field_name}")
                
                elif field_name == 'subject_name':
                    name_text = match.group(1).strip()
                    if len(name_text.split()) < 2:  # Должно быть минимум Фамилия Имя
                        errors.append(f"Неполное ФИО субъекта: {field_name}")
        
        # Дополнительные проверки
        if 'согласие на обработку персональных данных' not in content.lower():
            errors.append("Отсутствует заголовок согласия")
        
        if 'подпись' not in content.lower():
            errors.append("Отсутствует упоминание подписи")
        
        # Проверка на наличие пустых строк в критичных местах
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'даю согласие на обработку персональных данных' in line:
                # Следующая строка не должна быть пустой
                if i + 1 < len(lines) and not lines[i + 1].strip():
                    errors.append(f"Пустая строка после указания оператора (строка {i + 2})")
                break
        
        is_valid = len(errors) == 0
        return is_valid, errors
    
    def process_file(self, file_path: Path) -> None:
        """
        Обрабатывает один файл согласия
        
        Args:
            file_path: Путь к файлу
        """
        try:
            content = self.read_file_with_encoding(file_path)
            if content is None:
                self.errors_log.append(f"Ошибка чтения файла: {file_path.name}")
                self.incorrect_count += 1
                shutil.copy2(file_path, self.incorrect_dir / file_path.name)
                return
            
            is_valid, errors = self.validate_agreement(content, file_path.name)
            
            if is_valid:
                self.correct_count += 1
                shutil.copy2(file_path, self.correct_dir / file_path.name)
                print(f"✓ {file_path.name} - ПРАВИЛЬНО")
            else:
                self.incorrect_count += 1
                shutil.copy2(file_path, self.incorrect_dir / file_path.name)
                print(f"✗ {file_path.name} - ОШИБКИ: {', '.join(errors)}")
                self.errors_log.append(f"{file_path.name}: {', '.join(errors)}")
                
        except Exception as e:
            self.errors_log.append(f"Ошибка обработки {file_path.name}: {str(e)}")
            self.incorrect_count += 1
            shutil.copy2(file_path, self.incorrect_dir / file_path.name)
    
    def process_all_files(self) -> None:
        """
        Обрабатывает все файлы в входной папке
        """
        print("Начинаем анализ согласий на обработку персональных данных...")
        print("=" * 60)
        
        # Получаем список всех .txt файлов
        txt_files = list(self.input_dir.glob("*.txt"))
        
        if not txt_files:
            print("Файлы .txt не найдены в указанной папке!")
            return
        
        print(f"Найдено файлов для обработки: {len(txt_files)}")
        print()
        
        # Обрабатываем каждый файл
        for file_path in sorted(txt_files):
            self.process_file(file_path)
        
        print()
        print("=" * 60)
        print("АНАЛИЗ ЗАВЕРШЕН")
        print("=" * 60)
        print(f"Правильно оформленных согласий: {self.correct_count}")
        print(f"Неправильно оформленных согласий: {self.incorrect_count}")
        print(f"Всего обработано: {self.correct_count + self.incorrect_count}")
        print()
        print(f"Правильные согласия сохранены в: {self.correct_dir}")
        print(f"Неправильные согласия сохранены в: {self.incorrect_dir}")
    
    def generate_report(self) -> None:
        """
        Генерирует подробный отчет об анализе
        """
        report_path = self.output_dir / "analysis_report.txt"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("ОТЧЕТ ПО АНАЛИЗУ СОГЛАСИЙ НА ОБРАБОТКУ ПЕРСОНАЛЬНЫХ ДАННЫХ\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Дата анализа: {__import__('datetime').datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n")
            f.write(f"Исходная папка: {self.input_dir}\n")
            f.write(f"Выходная папка: {self.output_dir}\n\n")
            
            f.write("СТАТИСТИКА:\n")
            f.write("-" * 20 + "\n")
            f.write(f"Правильно оформленных согласий: {self.correct_count}\n")
            f.write(f"Неправильно оформленных согласий: {self.incorrect_count}\n")
            f.write(f"Всего обработано: {self.correct_count + self.incorrect_count}\n\n")
            
            if self.correct_count + self.incorrect_count > 0:
                success_rate = (self.correct_count / (self.correct_count + self.incorrect_count)) * 100
                f.write(f"Процент правильных согласий: {success_rate:.1f}%\n\n")
            
            f.write("ОБЯЗАТЕЛЬНЫЕ ПОЛЯ СОГЛАСИЯ (согласно ФЗ-152):\n")
            f.write("-" * 50 + "\n")
            f.write("1. ФИО субъекта персональных данных\n")
            f.write("2. Адрес субъекта персональных данных\n")
            f.write("3. Номер паспорта\n")
            f.write("4. Сведения о дате выдачи паспорта\n")
            f.write("5. Сведения о выдавшем паспорт органе\n")
            f.write("6. Наименование/ФИО оператора\n")
            f.write("7. Адрес оператора\n")
            f.write("8. Цель обработки персональных данных\n")
            f.write("9. Перечень персональных данных\n")
            f.write("10. Перечень действий с персональными данными\n")
            f.write("11. Срок действия согласия\n")
            f.write("12. Способ отзыва согласия\n")
            f.write("13. Подпись субъекта персональных данных\n\n")
            
            if self.errors_log:
                f.write("ОБНАРУЖЕННЫЕ ОШИБКИ:\n")
                f.write("-" * 20 + "\n")
                for error in self.errors_log:
                    f.write(f"• {error}\n")
            else:
                f.write("ОШИБОК НЕ ОБНАРУЖЕНО\n")
        
        print(f"Подробный отчет сохранен в: {report_path}")


def main():
    """
    Основная функция программы
    """
    # Определяем базовую директорию проекта
    current_dir = Path(__file__).parent
    project_root = current_dir.parent.parent  # Поднимаемся на 2 уровня выше
    
    # Пути к папкам (относительно корня проекта)
    input_directory = project_root / "ПрактическаяРабота№2r/Practice2Variants/Variant7"
    output_directory = current_dir / "practice2_results"
    
    print("ПРОГРАММА КЛАССИФИКАЦИИ СОГЛАСИЙ НА ОБРАБОТКУ ПЕРСОНАЛЬНЫХ ДАННЫХ")
    print("Практическая работа №2 - Вариант 7")
    print("=" * 70)
    print()
    
    # Создаем классификатор
    classifier = PersonalDataClassifier(input_directory, output_directory)
    
    # Обрабатываем все файлы
    classifier.process_all_files()
    
    # Генерируем отчет
    classifier.generate_report()
    
    print()
    print("Программа завершена успешно!")


if __name__ == "__main__":
    main()
