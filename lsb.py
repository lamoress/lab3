from PIL import Image
import math
import os

def file_to_binary(file_path):
    """
    Конвертирует файл в бинарное представление.

    :param file_path: Путь к файлу.
    :return: Бинарное представление файла.
    :raises FileNotFoundError: Если файл не найден.
    """
    try:
        with open(file_path, 'rb') as file:
            binary_data = ''.join(format(byte, '08b') for byte in file.read())
        return binary_data
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {file_path} не

from PIL import Image
import math
import os

def file_to_binary(file_path):
    """
    Конвертирует файл в бинарное представление.

    Путь к файлу.
    :return: Бинарное представление файла.
    :raises FileNotFoundError: Если файл не найден.
    """
    try:
        with open(file_path, 'rb') as file:
            binary_data = ''.join(format(byte, '08b') for byte in file.read())
        return binary_data
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {file_path} не найден.")

def psnr(original_image, encoded_image):
    """
    Рассчитывает отношение сигнал/шум (PSNR) между двумя изображениями.

    :param original_image: Оригинальное изображение.
    :param encoded_image: Закодированное изображение.
    :return: Значение PSNR.
    """
    mse = 0
    width, height = original_image.size

    for y in range(height):
        for x in range(width):
            original_pixel = original_image.getpixel((x, y))
            encoded_pixel = encoded_image.getpixel((x, y))
            mse += sum((p1 - p2) ** 2 for p1, p2 in zip(original_pixel, encoded_pixel)) / 3

    mse /= (width * height)
    if mse == 0:
        return float('inf')
    else:
        return 20 * math.log10(255 / math.sqrt(mse))

def encode_lsb(image_path, file_path):
    """
    Закодировать сообщение в изображение с помощью метода наименее значимого бита (LSB).

    :param image_path: Путь к изображению.
    :param file_path: Путь к файлу, который нужно закодировать.
    :return: Статус выполнения.
    """
    try:
        binary_data = file_to_binary(file_path)
        img = Image.open(image_path)
        width, height = img.size

        if len(binary_data) > width * height * 3:
            raise ValueError("Файл слишком большой для данного изображения.")

        binary_data += '1111111111111110'  # Добавляем конечный маркер

        data_index = 0
        for y in range(height):
            for x in range(width):
                pixel = list(img.getpixel((x, y)))
                for i in range(3):
                    if data_index < len(binary_data):
                        pixel[i] = pixel[i] & ~1 | int(binary_data[data_index])
                        data_index += 1
                img.putpixel((x, y), tuple(pixel))

                if data_index >= len(binary_data):
                    img.save("encoded_image.bmp")
                    return "Done"

        return "Ошибка"
    except FileNotFoundError as e:
        return str(e)

def decode_lsb(image_path):
    """
    Декодировать сообщение из изображения, закодированного методом наименее значимого бита (LSB).

    :param image_path: Путь к изображению.
    :return: Статус выполнения.
    """
    img = Image.open(image_path)
    binary_data = ''
    width, height = img.size

    for y in range(height):
        for x in range(width):
            pixel = img.getpixel((x, y))
            for value in pixel:
                binary_data += str(value & 1)

    binary_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    file_data = bytearray(int(byte, 2) for byte in binary_bytes)

    end_marker = bytearray([0xFF, 0xFE])  # Бинарный код '1111111111111110'
    end_index = file_data.find(end_marker)

    if end_index != -1:
        file_data = file_data[:end_index]
    with open("decoded_file.txt", 'wb') as file:
        file.write(file_data)
    return "Файл успешно извлечен."
