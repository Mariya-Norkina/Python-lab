from PIL import Image # type: ignore
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
            _, _, b = pixels[x, y]
            
            # Декодируем байт напрямую в символ ASCII
            char = chr(b)
            message += char
            
        print(f"Результат декодирования (1.1): {message}\n")

    except Exception as e:
        print(f"Ошибка в 1.1: {e}\n")

#ЗАДАНИЕ 1.2: Кодирование и декодирование (b0-R, b0-G, b0-B)
def task_1_2_process(input_image, text):
    print("--- Задание 1.2: LSB кодирование/декодирование ---")
    
    img = Image.open(input_image).convert('RGB')
    # Получаем плоский список пикселей
    pixels = list(img.getdata())
    
    # 1. Преобразование текста в биты (8 бит на символ)
    all_bits = []
    for char in text:
        # format(..., '08b') гарантирует 8 бит для каждого символа
        bits = [int(b) for b in format(ord(char), '08b')]
        all_bits.extend(bits)
    
    # ПУНКТ (a): Биты первого символа
    print(f"a. Биты первого символа '{text[0]}': {all_bits[:8]}")
    
    # ПУНКТ (b): Исходные значения пикселей (первые 3)
    print(f"b. Исходные значения пикселей: {pixels[:3]}")
    
    # 2. Кодирование (запись в 0-е биты каналов R, G, B)
    new_pixels = []
    bit_idx = 0
    total_bits = len(all_bits)
    
    for px in pixels:
        r, g, b = px
        channels = [r, g, b]
        for i in range(3):
            if bit_idx < total_bits:
                # Операция LSB: обнуляем 0-й бит и ставим бит сообщения
                channels[i] = (channels[i] & ~1) | all_bits[bit_idx]
                bit_idx += 1
        new_pixels.append(tuple(channels))
    
    # ПУНКТ (c): Измененные значения пикселей (первые 3)
    print(f"c. Измененные значения пикселей: {new_pixels[:3]}")
    
    # 3. Декодирование для проверки корректности
    extracted_bits = []
    for px in new_pixels:
        for channel in px:
            extracted_bits.append(channel & 1)
            
    decoded_text = ""
    for i in range(0, len(text) * 8, 8):
        byte_bits = extracted_bits[i:i+8]
        # Собираем строку из бит и превращаем в число (код символа)
        char_code = int("".join(map(str, byte_bits)), 2)
        decoded_text += chr(char_code)
        
    print(f"Результат декодирования (1.2): {decoded_text}")

#ЗАПУСК
if __name__ == "__main__":
    
    task_1_1_decode('new20.png', 'keys20.txt')
    task_1_2_process('new20.png', 'Maria')
    
