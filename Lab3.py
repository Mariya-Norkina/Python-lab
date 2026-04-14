from PIL import Image
from random import randint
import re

#ЗАДАНИЕ 1.1: Декодирование текста из синего канала
def task_1_1_decode(image_path, key_path):
    print("--- Задание 1.1: Извлечение текста из синего канала ---")
    try:
        img = Image.open(image_path).convert('RGB')
        pixels = img.load()

        # Чтение координат из файла
        coords = []
        with open(key_path, 'r') as f:
            for line in f:
                # Извлекаем числа из строк вида (52, 324)
                nums = re.findall(r'\d+', line)
                if len(nums) == 2:
                    coords.append((int(nums[0]), int(nums[1])))

        message = ""
        # Извлекаем байты согласно списку координат
        for i, (x, y) in enumerate(coords):
            # Нас интересует только синий канал (индекс 2)
            r, g, b = pixels[x, y]

            # print(_,_,b)
            
            # Декодируем байт напрямую в символ ASCII
            char = chr(b)
            message += char
            
        print(f"Результат декодирования (1.1): {message}\n")

    except Exception as e:
        print(f"Ошибка в 1.1: {e}\n")

#ЗАДАНИЕ 1.2: Кодирование и декодирование (b0-R, b0-G, b0-B)
def task_1_2_encode(input_image_path, text, output_image_path, key_file_path):
    print("--- Задание 1.2: LSB кодирование со случайными координатами ---")
    
    img = Image.open(input_image_path).convert('RGB')
    width, height = img.size
    pixels = img.load()
    
    # 1. Текст в биты (8 бит на символ)
    all_bits = []
    for char in text:
        bits = [int(b) for b in format(ord(char), '08b')]
        all_bits.extend(bits)
    
    # ДОКАЗАТЕЛЬСТВО (a): Биты первого символа
    if text:
        first_char_bits = [int(b) for b in format(ord(text[0]), '08b')]
        print(f"a. Биты первого символа '{text[0]}': {first_char_bits}")
    
    bit_idx = 0
    total_bits = len(all_bits)
    used_coords = set()
    coords_list = []
    
    original_pixels_preview = []
    changed_pixels_preview = []

    # 2. Процесс кодирования
    while bit_idx < total_bits:
        x = randint(0, width - 1)
        y = randint(0, height - 1)
        key = (x, y)
        
        if key not in used_coords:
            used_coords.add(key)
            coords_list.append(key)
            
            r, g, b = pixels[key]
            
            # Сохраняем для вывода (b) первые 3 задействованных пикселя
            if len(original_pixels_preview) < 3:
                original_pixels_preview.append((r, g, b))
            
            channels = [r, g, b]
            for i in range(3):
                if bit_idx < total_bits:
                    channels[i] = (channels[i] & ~1) | all_bits[bit_idx]
                    bit_idx += 1
            
            new_pixel = tuple(channels)
            pixels[key] = new_pixel
            
            # Сохраняем для вывода (c)
            if len(changed_pixels_preview) < 3:
                changed_pixels_preview.append(new_pixel)

    # ВЫВОД ДОКАЗАТЕЛЬСТВ (b и c)
    print(f"b. Исходные значения пикселей (первые 3 измененных): {original_pixels_preview}")
    print(f"c. Измененные значения пикселей (первые 3 измененных): {changed_pixels_preview}")

    # 3. Сохранение
    img.save(output_image_path)
    with open(key_file_path, 'w') as f:
        for coord in coords_list:
            f.write(f"{coord}\n")
    
    print(f"Закодировано бит: {total_bits}. Файлы сохранены.\n")

# === ДЕКОДИРОВАНИЕ (по созданным координатам) ===
def task_1_2_decode(image_path, key_path):
    print("--- Декодирование результата 1.2 по файлу ключа ---")
    img = Image.open(image_path).convert('RGB')
    pixels = img.load()
    
    # Читаем координаты из созданного txt
    coords = []
    with open(key_path, 'r') as f:
        for line in f:
            nums = re.findall(r'\d+', line)
            if len(nums) == 2:
                coords.append((int(nums[0]), int(nums[1])))
    
    # Извлекаем LSB из каждого канала указанных пикселей
    all_extracted_bits = []
    for x, y in coords:
        r, g, b = pixels[x, y]
        all_extracted_bits.extend([r & 1, g & 1, b & 1])
    
    # Собираем байты в текст
    decoded_text = ""
    for i in range(0, len(all_extracted_bits), 8):
        byte_bits = all_extracted_bits[i:i+8]
        if len(byte_bits) < 8: break
        char_code = int("".join(map(str, byte_bits)), 2)
        decoded_text += chr(char_code)
        
    print(f"Результат декодирования: {decoded_text}\n")

#ЗАПУСК
if __name__ == "__main__":
    
    task_1_1_decode('new20.png', 'keys20.txt')
    task_1_2_encode('pic.png', 'Name', 'output.png', 'output.txt')
    task_1_2_decode('output.png', 'output.txt')
    
