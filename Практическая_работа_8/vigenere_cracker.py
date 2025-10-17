#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Взлом шифра Виженера на основе кода из изображений
Практическая работа №8 - Вариант 7
"""

from collections import Counter

# Русский алфавит с пробелом как 34-я буква
ALPHABET = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ "

def char_to_index(c):
    """Преобразует символ в индекс в алфавите"""
    return ALPHABET.find(c)

def index_to_char(i):
    """Преобразует индекс в символ алфавита"""
    return ALPHABET[i % len(ALPHABET)]

def vigenere(text, key, encrypt=True):
    """Шифрование/расшифрование по методу Виженера"""
    result = []
    key_len = len(key)
    for i, c in enumerate(text):
        if c not in ALPHABET:
            result.append(c)
            continue
        text_idx = char_to_index(c)
        key_idx = char_to_index(key[i % key_len])
        if encrypt:
            new_idx = (text_idx + key_idx) % len(ALPHABET)
        else:
            new_idx = (text_idx - key_idx) % len(ALPHABET)
        result.append(index_to_char(new_idx))
    return ''.join(result)

def index_of_coincidence(text):
    """Вычисляет индекс совпадений для текста"""
    counts = Counter(text)
    length = len(text)
    if length < 2:
        return 0.0
    ic = sum(c * (c - 1) for c in counts.values()) / (length * (length - 1))
    return ic

def guess_key_length(ciphertext, max_len=20):
    """Определяет длину ключа методом индекса совпадений"""
    best_len = 1
    best_ic = 0
    expected_ic = 0.085576  # Для русского текста с пробелом
    
    for l in range(1, min(max_len + 1, len(ciphertext))):
        ics = []
        for i in range(l):
            segment = ciphertext[i::l]
            if len(segment) > 1:
                ics.append(index_of_coincidence(segment))
        avg_ic = sum(ics) / len(ics) if ics else 0
        if abs(avg_ic - expected_ic) < abs(best_ic - expected_ic):
            best_len = l
            best_ic = avg_ic
    return best_len

def find_key_segment(segment):
    """Находит ключ для сегмента методом частотного анализа"""
    # Порядок частотности русских букв (включая пробел)
    freq_order_ru = list(" ОЕАИНТСРЛВПМКУДЯЫЬЗБГЙЧХЮЖШЩЦФЭЪ")
    
    best_shift = 0
    best_score = float('-inf')
    
    for shift in range(len(ALPHABET)):
        decrypted = ''.join([index_to_char((char_to_index(c) - shift) % len(ALPHABET)) for c in segment])
        score = sum(decrypted.count(c) * (len(ALPHABET) - i) for i, c in enumerate(freq_order_ru))
        if score > best_score:
            best_score = score
            best_shift = shift
    return index_to_char(best_shift)

def break_vigenere(ciphertext):
    """Основная функция взлома шифра Виженера"""
    cleaned_text = ''.join([c for c in ciphertext.upper() if c in ALPHABET])
    key_length = guess_key_length(cleaned_text)
    print(f"Предположенная длина ключа: {key_length}")
    
    key = ''
    for i in range(key_length):
        segment = cleaned_text[i::key_length]
        key_char = find_key_segment(segment)
        key += key_char
    
    print(f"Найденный ключ: {key}")
    plaintext = vigenere(cleaned_text, key, encrypt=False)
    return plaintext, key

def main():
    """Основная функция программы"""
    print("ВЗЛОМ ШИФРА ВИЖЕНЕРА")
    print("Практическая работа №8 - Вариант 7")
    print("=" * 60)
    
    # Читаем зашифрованный текст
    try:
        with open("Вар7_original.txt", "r", encoding="utf-8") as f:
            cipher_text = f.read().strip()
    except FileNotFoundError:
        print("Файл Вар7_original.txt не найден!")
        return
    
    print("Шифр:")
    print(cipher_text)
    print()
    
    # Взламываем шифр
    plaintext, key = break_vigenere(cipher_text)
    
    print("\nРасшифрованный текст:")
    print(plaintext)
    
    # Сохраняем результат
    with open("decrypted_7.txt", "w", encoding="utf-8") as f:
        f.write(plaintext)
    
    print(f"\nРезультат сохранен в файл decrypted_7.txt")

if __name__ == "__main__":
    main()
