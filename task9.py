# Задача 9. Программная реализация кода Хаффмана.
import heapq
import math
from collections import Counter


def build_huffman(freq):
    heap = []
    number = 0
    for symbol, weight in sorted(freq.items()):
        if weight > 0:
            heap.append((weight, number, symbol))
            number += 1

    if not heap:
        raise ValueError("Словарь частот пустой")
    heapq.heapify(heap)

    while len(heap) > 1:
        w1, _, left = heapq.heappop(heap)
        w2, _, right = heapq.heappop(heap)
        heapq.heappush(heap, (w1 + w2, number, (left, right)))
        number += 1

    tree = heap[0][2]
    codes = {}

    def walk(node, code=""):
        if isinstance(node, str):
            codes[node] = code or "0"
        else:
            walk(node[0], code + "0")
            walk(node[1], code + "1")

    walk(tree)
    return tree, codes


def encode(text, codes):
    return "".join(codes[letter] for letter in text)


def decode(bits, tree):
    if isinstance(tree, str):
        if any(bit != "0" for bit in bits):
            raise ValueError("Некорректный код")
        return tree * len(bits)

    result = []
    node = tree
    for bit in bits:
        if bit not in "01":
            raise ValueError("Допустимы только 0 и 1")
        node = node[0] if bit == "0" else node[1]
        if isinstance(node, str):
            result.append(node)
            node = tree
    if node is not tree:
        raise ValueError("Незаконченное кодовое слово")
    return "".join(result)


def metrics(freq, codes):
    total = sum(freq.values())
    entropy = 0
    average = 0
    for letter, count in freq.items():
        if count > 0:
            p = count / total
            entropy -= p * math.log2(p)
            average += p * len(codes[letter])
    efficiency = entropy / average * 100
    redundancy = 100 - efficiency
    return entropy, average, efficiency, redundancy


if __name__ == "__main__":
    text = "ABCADE"
    freq = dict(Counter(text))
    tree, codes = build_huffman(freq)
    h, avg, eta, r = metrics(freq, codes)

    print("Частоты:", freq)
    print("Коды Хаффмана:", codes)
    print(f"Энтропия H(X): {h:.4f}")
    print(f"Средняя длина L: {avg:.4f}")
    print(f"Эффективность: {eta:.2f}%")
    print(f"Избыточность: {r:.2f}%")

    bits = encode(text, codes)
    restored = decode(bits, tree)
    print("Исходный текст:", text)
    print("Закодировано:", bits)
    print("Декодировано:", restored)
    assert restored == text
    print("Проверка кодирования и декодирования: OK")

    one_tree, one_codes = build_huffman({"X": 5})
    assert one_codes == {"X": "0"}
    assert decode(encode("XXXXX", one_codes), one_tree) == "XXXXX"
    print("Проверка одного символа: OK")
