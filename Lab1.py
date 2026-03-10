def input_matrix(r, c):
    """Функция для ручного ввода элементов матрицы."""
    print(f"Введите {r} строк по {c} чисел:")
    # Создаем список списков: для каждой строки считываем ввод, разбиваем по пробелам и конвертируем каждое число в float
    return [[float(x) for x in input(f"Стр {i+1}: ").split()] for i in range(r)]

def print_matrix(matrix, msg):
    """Функция для красивого вывода матрицы в консоль."""
    print(f"\n{msg}")
    for row in matrix:
        # f"{e:7.1f}" задает ширину 7 символов и 1 знак после запятой для выравнивания
        # *(...) распаковывает генератор, чтобы print вывел числа через пробел
        print(*(f"{e:7.1f}" for e in row))

def main():
    try:
        # Запрашиваем размеры матрицы
        r, c = int(input("Строк: ")), int(input("Столбцов: "))
        if r <= 0 or c <= 0:
            print("Размеры должны быть положительными.")
            return

        # 1. Ввод данных
        matrix = input_matrix(r, c)
        print_matrix(matrix, "Исходная:")
         # 2. Сортировка столбцов
        sorted_cols = sorted(zip(*matrix), key=sum)

        # 3. Обратное преобразование
        # zip(*sorted_cols) — возвращает столбцы в состояние строк
        # list(row) — превращает кортежи обратно в списки для удобства работы
        result = [list(row) for row in zip(*sorted_cols)]

        print_matrix(result, "Отсортированная (по возрастанию сумм столбцов):")

    except ValueError:
        print("Ошибка ввода: убедитесь, что вводите числа.")

if __name__ == "__main__":
    main()