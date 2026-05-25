from typing import List, Optional

class ListNode:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next

class AdvancedSorter:
    def __init__(self):
        pass

    # =========================================================
    # 1. ARRAY MERGE SORT (Virtual Sublists + Single tmpArray)
    # =========================================================
    def sort_array(self, arr: List[int]) -> List[int]:
        if len(arr) <= 1: return arr
        tmp_array = [0] * len(arr)  # Single temporary array
        self._rec_merge_sort(arr, 0, len(arr) - 1, tmp_array)
        return arr

    def _rec_merge_sort(self, arr, first, last, tmp_array):
        if first >= last: return
        mid = (first + last) // 2
        self._rec_merge_sort(arr, first, mid, tmp_array)
        self._rec_merge_sort(arr, mid + 1, last, tmp_array)
        self._merge_virtual(arr, first, mid, last, tmp_array)

    def _merge_virtual(self, arr, left_start, mid, right_end, tmp_array):
        a = left_start
        b = mid + 1
        m = left_start
        
        # Penggabungan elemen bersifat STABLE
        while a <= mid and b <= right_end:
            if arr[a] <= arr[b]:
                tmp_array[m] = arr[a]
                a += 1
            else:
                tmp_array[m] = arr[b]
                b += 1
            m += 1
            
        # Pindahkan sisa elemen dari sisi kiri
        while a <= mid:
            tmp_array[m] = arr[a]
            a += 1
            m += 1
            
        # Pindahkan sisa elemen dari sisi kanan
        while b <= right_end:
            tmp_array[m] = arr[b]
            b += 1
            m += 1
            
        # Salin kembali ke arr utama
        for i in range(left_start, right_end + 1):
            arr[i] = tmp_array[i]

    # =========================================================
    # 2. LINKED LIST MERGE SORT (Fast-Slow + Dummy Merge)
    # =========================================================
    def sort_linked_list(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None or head.next is None:
            return head
        
        right_head = self._split_linked_list(head)
        left_head = head
        
        left_sorted = self.sort_linked_list(left_head)
        right_sorted = self.sort_linked_list(right_head)
        
        return self._merge_linked_lists(left_sorted, right_sorted)

    def _split_linked_list(self, subList: ListNode) -> Optional[ListNode]:
        # Fast-slow pointer implementation
        midPoint = subList
        curNode = midPoint.next
        while curNode is not None:
            curNode = curNode.next
            if curNode is not None:
                midPoint = midPoint.next
                curNode = curNode.next
                
        rightList = midPoint.next
        midPoint.next = None  # Pemutus hubungan menjadi dua sublist
        return rightList

    def _merge_linked_lists(self, listA: Optional[ListNode], listB: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0)
        tail = dummy
        
        # Proses merge yang menempelkan node eksisting stabil tanpa inisiasi memori
        while listA is not None and listB is not None:
            if listA.data <= listB.data:
                tail.next = listA
                listA = listA.next
            else:
                tail.next = listB
                listB = listB.next
            tail = tail.next
            
        if listA is not None:
            tail.next = listA
        else:
            tail.next = listB
            
        return dummy.next

    # =========================================================
    # 3. QUICK SORT PARTITION (Median-of-Three Pivot)
    # =========================================================
    def partition_quick(self, arr: List[int], first: int, last: int) -> int:
        mid = (first + last) // 2
        
        # Mengelola pivot median-of-three 
        if arr[mid] < arr[first]:
            arr[first], arr[mid] = arr[mid], arr[first]
        if arr[last] < arr[first]:
            arr[first], arr[last] = arr[last], arr[first]
        if arr[last] < arr[mid]:
            arr[mid], arr[last] = arr[last], arr[mid]
            
        # Pindahkan nilai median untuk menjadi penanda 'first'
        arr[first], arr[mid] = arr[mid], arr[first]
        
        pivot = arr[first]
        left = first + 1
        right = last
        
        while left <= right:
            while left <= right and arr[left] < pivot:
                left += 1
            while left <= right and arr[right] >= pivot:
                right -= 1
                
            if left < right:
                arr[left], arr[right] = arr[right], arr[left]
                
        # Tempatkan pivot di posisi final
        arr[first] = arr[right]
        arr[right] = pivot
        
        return right

    # =========================================================
    # HEAP & SIFT-DOWN IMPLEMENTATION (Berdasarkan PDF Tambahan)
    # =========================================================
    def heapsort_inplace(self, arr: List[int]) -> List[int]:
        n = len(arr)
        if n <= 1: return arr
        
        # 1. Build max-heap in-place
        for i in range(n//2 - 1, -1, -1):
            self._sift_down(arr, n, i)
            
        # 2. Extract & sort
        for end in range(n-1, 0, -1):
            arr[0], arr[end] = arr[end], arr[0]
            self._sift_down(arr, end, 0)
        return arr

    def _sift_down(self, arr: List[int], heap_size: int, idx: int):
        while True:
            left = 2 * idx + 1
            right = 2 * idx + 2
            largest = idx
            
            # Cari nilai node yang lebih besar antara akar dengan dua daun bawahnya
            if left < heap_size and arr[left] >= arr[largest]:
                largest = left
            if right < heap_size and arr[right] >= arr[largest]:
                largest = right
                
            # Jika posisi salah, ganti tempat, dan ulangi 
            if largest != idx:
                arr[idx], arr[largest] = arr[largest], arr[idx]
                idx = largest
            else:
                break

    def is_complete_tree(self, arr: List[int]) -> bool:
        """Memvalidasi apakah array terurut memenuhi properti complete binary tree."""
        # Secara logikal linear array menaati kaidah complete tree ketika tak ditemukan gap None di tengah isi list.
        seen_none = False
        for val in arr:
            if val is None:
                seen_none = True
            elif seen_none:
                return False
        return True