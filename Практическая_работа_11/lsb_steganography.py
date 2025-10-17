#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Извлечение скрытой информации методом LSB стеганографии
Практическая работа №11 - Вариант 7
"""

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import zipfile
import io
import os
from typing import Tuple, Optional, List


class LSBSteganographyExtractor:
    """Класс для извлечения скрытой информации методом LSB"""
    
    def __init__(self, container_path: str, empty_container_path: str, expected_size: int):
        """
        Инициализация экстрактора
        
        Args:
            container_path: путь к контейнеру со скрытой информацией
            empty_container_path: путь к пустому контейнеру (первая часть ключа)
            expected_size: ожидаемый размер архива в байтах (вторая часть ключа)
        """
        self.container_path = container_path
        self.empty_container_path = empty_container_path
        self.expected_size = expected_size
        
        # Загружаем изображения
        self.container_img = Image.open(container_path)
        self.empty_img = Image.open(empty_container_path)
        
        # Преобразуем в numpy массивы
        self.container_array = np.array(self.container_img)
        self.empty_array = np.array(self.empty_img)
        
        print(f"Размер контейнера: {self.container_array.shape}")
        print(f"Размер пустого контейнера: {self.empty_array.shape}")
        
        # Проверяем, что размеры совпадают
        if self.container_array.shape != self.empty_array.shape:
            raise ValueError("Размеры контейнеров не совпадают!")
    
    def find_start_offset(self) -> Tuple[int, int]:
        """
        Находит горизонтальное смещение начальной точки на нулевой строке
        сравнивая контейнер с пустым контейнером
        
        Returns:
            Tuple[channel, offset]: канал и смещение начальной точки
        """
        print("Поиск начальной точки...")
        
        # Берем нулевую строку из обоих изображений
        container_row = self.container_array[0]
        empty_row = self.empty_array[0]
        
        # Проверяем каждый канал (R, G, B)
        for channel in range(3):  # 0=R, 1=G, 2=B
            container_channel = container_row[:, channel]
            empty_channel = empty_row[:, channel]
            
            # Ищем первое различие в LSB
            for offset in range(len(container_channel)):
                if (container_channel[offset] & 0x03) != (empty_channel[offset] & 0x03):
                    print(f"Найдена начальная точка: канал {['R', 'G', 'B'][channel]}, смещение {offset}")
                    return channel, offset
        
        raise ValueError("Начальная точка не найдена!")
    
    def extract_lsb_data(self, channel: int, start_offset: int) -> bytes:
        """
        Извлекает данные из LSB указанного канала
        
        Args:
            channel: канал (0=R, 1=G, 2=B)
            start_offset: смещение начальной точки
            
        Returns:
            bytes: извлеченные данные
        """
        print(f"Извлечение данных из канала {['R', 'G', 'B'][channel]}...")
        
        height, width, _ = self.container_array.shape
        data_bits = []
        
        # Проходим по столбцам слева направо, внутри столбца сверху вниз
        for col in range(start_offset, width):
            for row in range(height):
                # Извлекаем 2 младших бита
                pixel_value = self.container_array[row, col, channel]
                lsb_bits = pixel_value & 0x03  # 2 младших бита
                
                # Добавляем биты в список
                data_bits.append(lsb_bits)
        
        # Преобразуем биты в байты
        data_bytes = []
        for i in range(0, len(data_bits), 4):  # 4 бита = 1 байт (2 бита * 2 = 4 бита)
            if i + 3 < len(data_bits):
                # Собираем байт из 4 битов
                byte_value = (data_bits[i] << 6) | (data_bits[i+1] << 4) | (data_bits[i+2] << 2) | data_bits[i+3]
                data_bytes.append(byte_value)
        
        return bytes(data_bytes)
    
    def find_archive_end(self, data: bytes) -> int:
        """
        Находит конец архива, проверяя сигнатуры ZIP
        
        Args:
            data: извлеченные данные
            
        Returns:
            int: позиция конца архива
        """
        print("Поиск конца архива...")
        
        # Ищем сигнатуру ZIP (PK)
        zip_signatures = [b'PK\x03\x04', b'PK\x05\x06', b'PK\x07\x08']
        
        for i in range(len(data) - 4):
            chunk = data[i:i+4]
            if chunk in zip_signatures:
                # Проверяем, что это конец архива
                if chunk == b'PK\x05\x06':  # End of central directory
                    print(f"Найден конец архива на позиции {i}")
                    return i + 22  # Размер EOCD записи
        
        # Если не нашли сигнатуру, используем ожидаемый размер
        print(f"Сигнатура не найдена, используем ожидаемый размер: {self.expected_size}")
        return self.expected_size
    
    def extract_archive(self, data: bytes, end_pos: int) -> Optional[bytes]:
        """
        Извлекает ZIP архив из данных
        
        Args:
            data: извлеченные данные
            end_pos: позиция конца архива
            
        Returns:
            bytes: данные архива или None
        """
        print(f"Извлечение архива (размер: {end_pos} байт)...")
        
        archive_data = data[:end_pos]
        
        # Проверяем, что это валидный ZIP
        try:
            with zipfile.ZipFile(io.BytesIO(archive_data), 'r') as zip_file:
                file_list = zip_file.namelist()
                print(f"Файлы в архиве: {file_list}")
                return archive_data
        except zipfile.BadZipFile:
            print("Ошибка: данные не являются валидным ZIP архивом")
            return None
    
    def visualize_steganography(self, channel: int, start_offset: int, end_pos: int):
        """
        Создает визуализацию пространственного расположения скрытой информации
        
        Args:
            channel: канал с данными
            start_offset: смещение начальной точки
            end_pos: позиция конца данных
        """
        print("Создание визуализации...")
        
        height, width, _ = self.container_array.shape
        
        # Создаем маску для визуализации
        mask = np.zeros((height, width), dtype=np.uint8)
        
        # Вычисляем количество пикселей, необходимых для данных
        bits_needed = end_pos * 8  # 8 бит на байт
        pixels_needed = bits_needed // 2  # 2 бита на пиксель
        
        # Отмечаем пиксели, содержащие скрытые данные
        pixels_used = 0
        for col in range(start_offset, width):
            for row in range(height):
                if pixels_used < pixels_needed:
                    mask[row, col] = 255
                    pixels_used += 1
                else:
                    break
            if pixels_used >= pixels_needed:
                break
        
        # Создаем визуализацию
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Оригинальное изображение
        axes[0, 0].imshow(self.container_img)
        axes[0, 0].set_title('Оригинальный контейнер')
        axes[0, 0].axis('off')
        
        # Пустой контейнер
        axes[0, 1].imshow(self.empty_img)
        axes[0, 1].set_title('Пустой контейнер')
        axes[0, 1].axis('off')
        
        # Маска скрытых данных
        axes[1, 0].imshow(mask, cmap='hot')
        axes[1, 0].set_title(f'Область скрытых данных (канал {["R", "G", "B"][channel]})')
        axes[1, 0].axis('off')
        
        # Наложение маски на оригинал
        overlay = self.container_array.copy()
        overlay[:, :, channel] = np.maximum(overlay[:, :, channel], mask)
        axes[1, 1].imshow(overlay)
        axes[1, 1].set_title('Наложение области данных')
        axes[1, 1].axis('off')
        
        plt.tight_layout()
        plt.savefig('steganography_visualization.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("Визуализация сохранена как 'steganography_visualization.png'")
    
    def count_cats_in_archive(self, archive_data: bytes) -> int:
        """
        Подсчитывает количество котиков в архиве
        
        Args:
            archive_data: данные архива
            
        Returns:
            int: количество изображений котиков
        """
        print("Подсчет котиков в архиве...")
        
        try:
            with zipfile.ZipFile(io.BytesIO(archive_data), 'r') as zip_file:
                file_list = zip_file.namelist()
                
                # Подсчитываем изображения (предполагаем, что это jpg, png, gif)
                image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
                cat_count = 0
                
                for filename in file_list:
                    if any(filename.lower().endswith(ext) for ext in image_extensions):
                        cat_count += 1
                        print(f"Найден котик: {filename}")
                
                return cat_count
                
        except zipfile.BadZipFile:
            print("Ошибка при чтении архива")
            return 0
    
    def extract_and_analyze(self):
        """
        Основной метод для извлечения и анализа скрытой информации
        """
        print("=" * 60)
        print("ИЗВЛЕЧЕНИЕ СКРЫТОЙ ИНФОРМАЦИИ МЕТОДОМ LSB")
        print("Практическая работа №11 - Вариант 7")
        print("=" * 60)
        
        # 1. Находим начальную точку
        channel, start_offset = self.find_start_offset()
        
        # 2. Извлекаем данные
        data = self.extract_lsb_data(channel, start_offset)
        print(f"Извлечено {len(data)} байт данных")
        
        # 3. Находим конец архива
        end_pos = self.find_archive_end(data)
        
        # 4. Извлекаем архив
        archive_data = self.extract_archive(data, end_pos)
        
        if archive_data is None:
            print("Не удалось извлечь архив")
            return
        
        # 5. Сохраняем архив
        with open('extracted_archive.zip', 'wb') as f:
            f.write(archive_data)
        print("Архив сохранен как 'extracted_archive.zip'")
        
        # 6. Создаем визуализацию
        self.visualize_steganography(channel, start_offset, end_pos)
        
        # 7. Подсчитываем котиков
        cat_count = self.count_cats_in_archive(archive_data)
        
        # 8. Выводим результаты
        print("\n" + "=" * 60)
        print("РЕЗУЛЬТАТЫ АНАЛИЗА")
        print("=" * 60)
        print(f"Канал с данными: {['R', 'G', 'B'][channel]}")
        print(f"Горизонтальное смещение: {start_offset}")
        print(f"Размер архива: {len(archive_data)} байт")
        print(f"Ожидаемый размер: {self.expected_size} байт")
        print(f"Количество котиков в лесу: {cat_count}")
        
        return {
            'channel': channel,
            'start_offset': start_offset,
            'archive_size': len(archive_data),
            'expected_size': self.expected_size,
            'cat_count': cat_count
        }


def main():
    """Основная функция"""
    # Параметры для варианта 7
    container_path = "catsInforest7.png"
    empty_container_path = "emptyContainer.png"
    expected_size = 298254  # Размер архива для варианта 7
    
    # Проверяем наличие файлов
    if not os.path.exists(container_path):
        print(f"Ошибка: файл {container_path} не найден")
        return
    
    if not os.path.exists(empty_container_path):
        print(f"Ошибка: файл {empty_container_path} не найден")
        return
    
    # Создаем экстрактор и запускаем анализ
    extractor = LSBSteganographyExtractor(container_path, empty_container_path, expected_size)
    results = extractor.extract_and_analyze()
    
    return results


if __name__ == "__main__":
    main()
