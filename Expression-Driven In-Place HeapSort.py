from typing import List, Optional
from collections import deque

class ExprHeapSorter:
    def __init__(self, expr_str: str):
        self.expr = expr_str
        self.values = []

    def parse_and_evaluate(self) -> List[int]:
        """Membangun pohon ekspresi, mengevaluasi, mengembalikan list nilai integer intermediate/final."""
        tokens = deque(self.expr)
        root = self._build_tree(tokens)
        self.values = self._eval_tree(root)
        return self.values

    def _build_tree(self, tokens: deque) -> Optional[dict]:
        """Implementasi rekursif pembentukan pohon dari infix token."""
        if not tokens: 
            return None
            
        token = tokens.popleft()
        
        # Token kiri '(' menandakan awal parenthesised sub-tree
        if token == '(':
            node = {}
            node['left'] = self._build_tree(tokens)
            node['val'] = tokens.popleft()   # Node Operator
            node['right'] = self._build_tree(tokens)
            tokens.popleft()                 # Buang terminal ')' dari stack token
            return node
        else:
            # Nilai skalar/operand
            return {'val': token}

    def _eval_tree(self, node: Optional[dict]) -> List[int]:
        """Evaluasi postorder secara mendalam menuruni node sub-tree. 
           Mengembalikan susunan akumulasi list hasil komputasi [kiri, kanan, parent]."""
        if not node:
            return []
            
        # Pengecekan status Leaf (Operand Numerik murni)
        if 'left' not in node and 'right' not in node:
            return [int(node['val'])]
            
        left_vals = self._eval_tree(node.get('left'))
        right_vals = self._eval_tree(node.get('right'))
        
        # Ekstrak hasil perhitungan level anak terdalam
        l_result = left_vals[-1] if left_vals else 0
        r_result = right_vals[-1] if right_vals else 0
        op = node['val']
        
        if op == '+': res = l_result + r_result
        elif op == '-': res = l_result - r_result
        elif op == '*': res = l_result * r_result
        elif op == '/': 
            if r_result == 0: 
                raise ValueError("Division by zero")
            res = l_result // r_result # Integer division
            
        return left_vals + right_vals + [res]

    def heapsort_inplace(self, arr: List[int]) -> List[int]:
        """Mengurutkan array secara ascending menggunakan in-place heapsort"""
        n = len(arr)
        if n <= 1: 
            return arr
            
        # 1. Build max-heap in-place dari simpul terdalam menuju node root
        for i in range(n//2 - 1, -1, -1):
            self._sift_down(arr, n, i)
            
        # 2. Extract & sort root ke bagian paling akhir dari batas maya theSeq secara logis
        for end in range(n-1, 0, -1):
            arr[0], arr[end] = arr[end], arr[0]
            self._sift_down(arr, end, 0)
            
        return arr

    def _sift_down(self, arr: List[int], heap_size: int, idx: int):
        """Merotasi posisi memori heap ke bawah secara efisien in-place"""
        while True:
            left = 2 * idx + 1
            right = 2 * idx + 2
            largest = idx
            
            # Cari child yang nilainya lebih masif dari parent
            if left < heap_size and arr[left] > arr[largest]:
                largest = left
            if right < heap_size and arr[right] > arr[largest]:
                largest = right
                
            if largest != idx:
                arr[idx], arr[largest] = arr[largest], arr[idx]
                idx = largest
            else:
                break

    def is_complete_tree(self, arr: List[int]) -> bool:
        """Memvalidasi array untuk kelayakan properti complete binary tree."""
        n = len(arr)
        for i in range(n):
            left = 2 * i + 1
            right = 2 * i + 2
            # Dalam pemetaan logis heap statik, loncatan NULL ke simpul tak valid diprohibit
            if left < n and arr[left] is None:
                return False
            if right < n and arr[right] is None:
                return False
        return True