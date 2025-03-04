def count_subarrays_with_median(N, B, A):
    count = 0

    for i in range(N):
        if A[i] == B:
            left_count = 0
            right_count = 0

            # Расширяем подотрезок в обе стороны
            l, r = i, i

            while l >= 0 and r < N:
                if A[l] < B:
                    left_count += 1
                elif A[l] > B:
                    right_count += 1

                if A[r] < B:
                    left_count += 1
                elif A[r] > B:
                    right_count += 1

                # Проверяем, что длина подотрезка нечетная
                if (r - l + 1) % 2 == 1:
                    # Проверяем, что количество меньше и больше B одинаково



                     count += 1

                # Расширяем подотрезок
                l -= 1
                r += 1

    return count


# Чтение входных данных
N, B = map(int, input().split())
A = list(map(int, input().split()))

# Вывод результата
result = count_subarrays_with_median(N, B, A)
print(result)

# Чтение входных данных
N, B = map(int, input().split())
A = list(map(int, input().split()))

# Вывод результата
result = count_subarrays_with_median(N, B, A)
print(result)





















