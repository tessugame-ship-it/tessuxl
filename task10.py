# Задача 10. Исследование реального русского текста.
# Пробелы, регистр и знаки препинания учитываются.
import json
from collections import Counter
from task9 import build_huffman, encode, decode, metrics

text = (
    "Информация окружает нас каждый день. Мы читаем сообщения, смотрим видео, "
    "общаемся с друзьями и изучаем новые темы. Все эти данные можно сохранить "
    "в памяти компьютера. При этом разные символы встречаются с разной частотой. "
    "Например, пробелы и некоторые буквы используются гораздо чаще других. "
    "Алгоритм Хаффмана помогает уменьшить размер данных: частым символам он "
    "назначает короткие двоичные коды, а редким — более длинные. "
    "Такой способ сжатия позволяет сохранить исходный текст без потери информации. "
    "После декодирования мы получаем точно такое же сообщение."
)

if len(text) < 300:
    raise ValueError("Текст должен содержать не менее 300 символов")

freq = dict(Counter(text))
tree, codes = build_huffman(freq)
h, avg, eta, r = metrics(freq, codes)
bits = encode(text, codes)
assert decode(bits, tree) == text

# Упаковываем двоичный код в целое число байтов.
padding = (8 - len(bits) % 8) % 8
padded_bits = bits + "0" * padding
packed = bytearray()
for i in range(0, len(padded_bits), 8):
    packed.append(int(padded_bits[i:i + 8], 2))

# Способ хранения: поток битов + таблица кодов JSON (UTF-8)
# + 4 байта на количество символов + 1 байт на число добавленных нулей.
code_table = json.dumps(codes, ensure_ascii=False).encode("utf-8")
header = len(text).to_bytes(4, "big") + bytes([padding])

original_bytes = len(text.encode("utf-8"))
compressed_bytes = len(packed)
overhead_bytes = len(code_table) + len(header)
total_bytes = compressed_bytes + overhead_bytes

print("Задача 10. Сжатие русского текста")
print("Количество символов:", len(text))
print("Различных символов:", len(freq))
print("Частоты и коды символов:")
for symbol, count in sorted(freq.items(), key=lambda x: (-x[1], x[0])):
    print(f"{symbol!r}: частота={count}, код={codes[symbol]}")

print(f"\nЭнтропия H(X): {h:.4f} бит/символ")
print(f"Средняя длина L: {avg:.4f} бит/символ")
print(f"Эффективность: {eta:.2f}%")
print(f"Избыточность: {r:.2f}%")
print(f"Исходный текст UTF-8: {original_bytes} байт")
print(f"Код Хаффмана: {len(bits)} бит")
print(f"Упакованный поток: {compressed_bytes} байт")
print(f"Выравнивание последнего байта: {padding} бит")
print(f"Таблица кодов JSON: {len(code_table)} байт")
print(f"Заголовок: {len(header)} байт")
print(f"Итог со служебными данными: {total_bytes} байт")
print(f"Экономия без таблицы: {(1 - compressed_bytes / original_bytes) * 100:.2f}%")
print(f"Экономия с таблицей: {(1 - total_bytes / original_bytes) * 100:.2f}%")

if total_bytes < original_bytes:
    print("Вывод: сжатие выгодно даже с учётом служебных данных.")
else:
    print("Вывод: из-за служебных данных такой текст сжимать невыгодно.")
print("Проверка восстановления текста: OK")
