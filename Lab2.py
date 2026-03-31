import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore
from scipy.io import wavfile
from scipy import signal
import time
import sys

def process_audio():
    # Добавляем время вычисления
    start_time = time.time()
    
    try:
        # 1. Чтение файла
        file_path = '20.wav' 
        sample_rate, data = wavfile.read(file_path)

        # Если файл стерео, берем один канал
        if len(data.shape) > 1:
            data = data[:, 0]

        # 2. Ввод количества отсчетов
        try:
            n_samples_input = int(input(f"Введите количество отсчетов (доступно {len(data)}): "))
            if n_samples_input <= 0 or n_samples_input > len(data):
                print("Некорректное число, выбрано максимальное количество.")
                n_samples = len(data)
            else:
                n_samples = n_samples_input
        except ValueError:
            print("Ошибка ввода. Использованы все отсчеты.")
            n_samples = len(data)

        # Ограничиваем данные
        data_slice = data[:n_samples]
        time_axis = np.linspace(0, n_samples / sample_rate, num=n_samples)

        # Создаем фигуру с несколькими графиками
        fig, axs = plt.subplots(2, 2, figsize=(15, 10))
        plt.subplots_adjust(hspace=0.4, wspace=0.3)

        # --- 2.2 Осциллограмма (Временная область) ---
        axs[0, 0].plot(time_axis, data_slice, color='steelblue', alpha=0.8, linewidth=0.5)
        axs[0, 0].set_title("Осциллограмма звукового сигнала")
        axs[0, 0].set_xlabel("Время (сек)")
        axs[0, 0].set_ylabel("Амплитуда")
        axs[0, 0].grid(True)
        
        # --- 2.1 & 2.3 Время-частотный спектр (Спектрограмма) ---
        # Задание 20 - спектрограмма
        frequencies, times, spectrogram = signal.spectrogram(data_slice, sample_rate)
        
        # Используем логарифмическую шкалу (dB) для наглядности
        im = axs[0, 1].pcolormesh(times, frequencies, 10 * np.log10(spectrogram + 1e-10), 
                                  shading='gouraud', cmap='magma')
        axs[0, 1].set_title("Время-частотный спектр (Спектрограмма)")
        axs[0, 1].set_xlabel("Время (сек)")
        axs[0, 1].set_ylabel("Частота (Гц)")
        fig.colorbar(im, ax=axs[0, 1], label='Мощность (дБ)')

        # --- Доп. Спектральный анализ (Амплитудный спектр FFT) ---
        fft_spectrum = np.fft.rfft(data_slice)
        fft_freqs = np.fft.rfftfreq(n_samples, 1/sample_rate)
        
        axs[1, 0].scatter(fft_freqs, np.abs(fft_spectrum), s=1, color='darkred', alpha=0.6)
        axs[1, 0].set_title("Спектральный анализ (БПФ)")
        axs[1, 0].set_xlabel("Частота (Гц)")
        axs[1, 0].set_ylabel("Амплитуда спектра")
        axs[1, 0].grid(True)

        # --- 2.4 Гистограмма значений ---
        axs[1, 1].hist(data_slice, bins=50, color='forestgreen', edgecolor='black')
        axs[1, 1].set_title("Гистограмма распределения амплитуд")
        axs[1, 1].set_xlabel("Значение амплитуды (отсчета)")
        axs[1, 1].set_ylabel("Частота попадания (кол-во)")
        axs[1, 1].grid(axis='y', alpha=0.75)

        # Вывод времени вычисления
        print(time.time() - start_time, "seconds")

        plt.show()

    except FileNotFoundError:
        print("Ошибка: Файл '20.wav' не найден в папке с программой.")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")

if __name__ == "__main__":
    process_audio()