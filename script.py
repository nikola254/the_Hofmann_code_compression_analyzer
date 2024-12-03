import heapq
from collections import defaultdict
import os
from scipy.stats import entropy

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq
    
def build_frequency_table(text):
    frequency = defaultdict(int)
    for char in text:
        frequency[char] += 1
    return frequency

def build_huffman_tree(frequency):
    heap = []
    for char, freq in frequency.items():
        node = Node(char, freq)
        heapq.heappush(heap, node)

    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        merged = Node(None, lo.freq + hi.freq)
        merged.left = lo
        merged.right = hi
        heapq.heappush(heap, merged)

    return heap[0]

def build_codes_helper(root, current_code, codes):
    if root == None:
        return

    if root.char != None:
        codes[root.char] = current_code

    build_codes_helper(root.left, current_code + "0", codes)
    build_codes_helper(root.right, current_code + "1", codes)

def build_codes(root):
    codes = {}
    build_codes_helper(root, "", codes)
    return codes

def huffman_encoding(text):
    frequency = build_frequency_table(text)
    root = build_huffman_tree(frequency)
    codes = build_codes(root)
    encoded_text = ''.join(codes[char] for char in text)
    return encoded_text, root

def huffman_decoding(encoded_text, root):
    decoded_text = ''
    current_node = root

    for bit in encoded_text:
        if bit == '0':
            current_node = current_node.left
        else:
            current_node = current_node.right

        if current_node.char != None:
            decoded_text += current_node.char
            current_node = root

    return decoded_text

def encode_file(file_path):
    with open(file_path, 'rb') as file:
        binary_data = file.read()
    text = binary_data.decode('latin-1')  
    encoded_text, tree = huffman_encoding(text)
    
    encoded_file_path = file_path + '.huf'
    with open(encoded_file_path, 'wb') as encoded_file:
        encoded_file.write(encoded_text.encode('latin-1'))
    
    return tree, encoded_file_path

def decode_file(file_path, tree):
    with open(file_path, 'rb') as file:
        binary_data = file.read()
    text = binary_data.decode('latin-1')
    decoded_text = huffman_decoding(text, tree)
    
    decoded_file_path = file_path.rsplit('.', 1)[0] + '_decoded'
    with open(decoded_file_path, 'wb') as decoded_file:
        decoded_file.write(decoded_text.encode('latin-1'))
    
    return decoded_file_path

def calculate_entropy(file_path):
    with open(file_path, 'rb') as file:
        binary_data = file.read()
    frequencies = defaultdict(int)
    total_bytes = len(binary_data)
    
    for byte in binary_data:
        frequencies[byte] += 1
    
    probabilities = [freq / total_bytes for freq in frequencies.values()]
    return entropy(probabilities, base=2)

def compare_entropies(original, encoded, decoded):
    original_entropy = calculate_entropy(original)
    encoded_entropy = calculate_entropy(encoded)
    decoded_entropy = calculate_entropy(decoded)
    
    print(f"Исходная энтропия: {original_entropy}")
    print(f"Энтропия после сжатия: {encoded_entropy}")
    print(f"Энтропия после декодирования: {decoded_entropy}")
    
    efficiency = (original_entropy - encoded_entropy) / original_entropy * 100
    print(f"\nЭффективность сжатия: {efficiency:.2f}%")
    
    # reconstruction_accuracy = abs(original_entropy - decoded_entropy) / original_entropy * 100
    # print(f"Reconstruction accuracy: {reconstruction_accuracy:.2f}%")

# Пример использования
word_file = 'C:/Ti/test.docx'
excel_file = 'C:/Ti/test1.xlsx'

_, word_encoded_path = encode_file(word_file)
word_decoded_path = decode_file(word_encoded_path, encode_file(word_file)[0])

_, excel_encoded_path = encode_file(excel_file)
excel_decoded_path = decode_file(excel_encoded_path, encode_file(excel_file)[0])

print("\nWord file results:")
compare_entropies(word_file, word_encoded_path, word_decoded_path)

print("\nExcel file results:")
compare_entropies(excel_file, excel_encoded_path, excel_decoded_path)
