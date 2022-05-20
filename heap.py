#print('hi')
class Heap:
    N: int = 0
    array = [None]
    def __init__(self) -> None:
        pass
    def insert(self, v: int) -> None:
        self.N += 1
        self.array.append(v)
        self.upheap(self.N)
    def upheap(self, i) -> None:
        if i > 1:
            parent_index = self.parent(i)
            if self.array[parent_index] < self.array[i]:
                self.swap(i, parent_index)
                self.upheap(parent_index)
    #removes the root
    def remove(self) -> int:
        if self.N > 0:
            removed = self.array[1]
            #removed the last element at N and put on top
            if self.N > 1:
                self.array[1] = self.array.pop()
                self.N -= 1
                self.downheap(1)
            else:
                self.array.pop()
                self.N -= 1
            return removed
        else:
            return None
    def downheap(self, i: int) -> None:
        left_index, right_index = self.children(i)
        child_index = left_index
        if child_index > self.N:
            return
        if right_index <= self.N and self.array[right_index] > self.array[left_index]:
            child_index = right_index
        if self.array[child_index] > self.array[i]:
            self.swap(i, child_index)
            self.downheap(child_index)
    
    def parent(self, i: int) -> int:
        return int ((i-i%2) / 2)
    def children(self, i: int):
        return i*2, i*2 +1
    def swap(self, i, j):
        temp = self.array[i]
        self.array[i] = self.array[j]
        self.array[j] = temp
    def print(self) -> None:
        for x in self.array:
            print(x)


heap: Heap = Heap()
for i in range(0,2):
    heap.insert(2)
    heap.insert(4)
    heap.insert(8)
    heap.insert(12)
    heap.print()
    print('Removed: ', heap.remove())
    heap.insert(7)
    print('Removed: ', heap.remove())
    print('Removed: ', heap.remove())
    print('Removed: ', heap.remove())
    print('Removed: ', heap.remove())
    heap.print()


