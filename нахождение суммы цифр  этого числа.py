from typing import List

def min_transport_platforms(weights: List[int], limit: int) -> int:
    weights.sort()  # Сортируем массив весов
    left: int = 0  # Указатель на легкого робота
    right: int = len(weights) - 1  # Указатель на тяжелого робота
    platforms: int = 0  # Счетчик платформ

    while left <= right:
        if weights[left] + weights[right] <= limit:
            left += 1  # Перевозим легкого робота
        right -= 1  # Перевозим тяжелого робота
        platforms += 1  # Платформа используется

    return platforms

def main() -> None:
    input_weights: str = input("Введите веса роботов через пробел: ").strip()
    limit: int = int(input("Введите лимит грузоподъёмности платформы: ").strip())

    # Преобразование массива строк в массив целых чисел
    weights: List[int] = list(map(int, input_weights.split()))

    # Вычисление минимального количества платформ
    result: int = min_transport_platforms(weights, limit)

    # Вывод результата
    print(result)

if __name__ == "__main__":
    main()
