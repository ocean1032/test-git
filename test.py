class Student:
    def __init__(self, id, name, math, literature):
        self.id = id
        self.name = name
        self.mathScore = math
        self.literatureScore = literature
        self.averageScore = (math + literature) / 2

class Node:
    def __init__(self, student):
        self.data = student
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    # (2.0 điểm) Hàm nhập thông tin
    def add_student(self, student):
        new_node = Node(student)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    # (1.0 điểm) In danh sách
    def display(self):
        current = self.head
        while current:
            s = current.data
            print(f"{s.id} - {s.name} | Math: {s.mathScore} | Literature: {s.literatureScore} | Avg: {s.averageScore:.2f}")
            current = current.next

    # (2.0 điểm) Tìm học sinh có điểm TB cao nhất
    def find_max_average(self):
        if not self.head:
            return None
        max_node = self.head
        current = self.head.next
        while current:
            if current.data.averageScore > max_node.data.averageScore:
                max_node = current
            current = current.next
        return max_node.data

    # (2.0 điểm) Sắp xếp theo điểm trung bình tăng dần
    def sort_by_average(self):
        if not self.head or not self.head.next:
            return
        changed = True
        while changed:
            changed = False
            prev = None
            curr = self.head
            while curr and curr.next:
                next_node = curr.next
                if curr.data.averageScore > next_node.data.averageScore:
                    # Swap
                    if prev:
                        prev.next = next_node
                    else:
                        self.head = next_node
                    curr.next = next_node.next
                    next_node.next = curr
                    changed = True
                    prev = next_node
                else:
                    prev = curr
                    curr = curr.next

    # (2.0 điểm) Danh sách học sinh điểm Toán > 7
    def filter_math_above_7(self):
        result = LinkedList()
        current = self.head
        while current:
            if current.data.mathScore > 7:
                result.add_student(current.data)
            current = current.next
        return result

# (1.0 điểm) Menu chọn lựa
def menu():
    print("\n--- MENU ---")
    print("1. Nhập danh sách học sinh mẫu")
    print("2. In danh sách học sinh")
    print("3. Học sinh có điểm TB cao nhất")
    print("4. Sắp xếp theo điểm TB tăng dần")
    print("5. Lọc học sinh có điểm Toán > 7")
    print("0. Thoát")

# ---------- Chương trình chính ----------
def main():
    ds = LinkedList()
    while True:
        menu()
        choice = input("Chọn: ")
        if choice == '1':
            # Thêm mẫu 10 học sinh
            samples = [
                Student(1, "An", 8, 6),
                Student(2, "Bình", 9, 7),
                Student(3, "Cường", 6, 5),
                Student(4, "Dũng", 7, 8),
                Student(5, "Em", 9, 9),
                Student(6, "Giang", 4, 6),
                Student(7, "Hoa", 8, 9),
                Student(8, "Khoa", 7, 5),
                Student(9, "Linh", 5, 6),
                Student(10, "Minh", 9, 8),
                Student(11, "Nam", 6, 6)
            ]
            for s in samples:
                ds.add_student(s)
            print(">> Đã thêm học sinh mẫu.")
        elif choice == '2':
            ds.display()
        elif choice == '3':
            hs = ds.find_max_average()
            print(f"Học sinh điểm TB cao nhất: {hs.name} - Avg: {hs.averageScore:.2f}")
        elif choice == '4':
            ds.sort_by_average()
            print(">> Đã sắp xếp.")
        elif choice == '5':
            filtered = ds.filter_math_above_7()
            print("Học sinh có điểm toán > 7:")
            filtered.display()
        elif choice == '0':
            break
        else:
            print("Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main()
