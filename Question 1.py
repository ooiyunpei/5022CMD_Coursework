import time
import random

class hashNode:

    # constructor
    def __init__(self, key, value):
        self.key = key
        self.value = value


class hashMap:

    # constructor
    def __init__(self, capacity=20):
        self.capacity = capacity
        self.size = 0
        self.arr = [None] * self.capacity
        self.dummy = hashNode(-1, -1)

    # hash function
    def hashCode(self, key):
        return key % self.capacity

    # insert key-value pair
    def insertNode(self, key, value):
        temp = hashNode(key, value)
        hashIndex = self.hashCode(key)

        while self.arr[hashIndex] is not None and \
                self.arr[hashIndex].key != key and \
                self.arr[hashIndex].key != -1:
            hashIndex = (hashIndex + 1) % self.capacity

        if self.arr[hashIndex] is None or \
                self.arr[hashIndex].key == -1:
            self.size += 1
        self.arr[hashIndex] = temp

    # delete by key
    def deleteNode(self, key):
        hashIndex = self.hashCode(key)

        while self.arr[hashIndex] is not None:
            if self.arr[hashIndex].key == key:
                temp = self.arr[hashIndex]
                self.arr[hashIndex] = self.dummy
                self.size -= 1
                return temp.value
            hashIndex = (hashIndex + 1) % self.capacity

        return -1

    # get value by key
    def get(self, key):
        hashIndex = self.hashCode(key)
        counter = 0

        while self.arr[hashIndex] is not None:
            if counter > self.capacity:
                return -1
            if self.arr[hashIndex].key == key:
                return self.arr[hashIndex].value
            hashIndex = (hashIndex + 1) % self.capacity
            counter += 1

        return -1

    # return map size
    def sizeofMap(self):
        return self.size

    # check if map is empty
    def isEmpty(self):
        return self.size == 0

    # display all key-value pairs
    def display(self):
        for node in self.arr:
            if node is not None and node.key != -1:
                print(f"{node.key} {node.value}")

class Medicine:
    def __init__(self, medicine_id, name, category, price, stock):
        self.medicine_id = medicine_id
        self.name = name
        self.category = category
        self.price = price
        self.stock = stock

    def __str__(self):
        return (f"ID: {self.medicine_id}, "
                f"Name: {self.name}, "
                f"Category: {self.category}, "
                f"Price: RM{self.price:.2f}, "
                f"Stock: {self.stock}")


def add_random_medicines(inventory, medicine_list, n=5):
    # Collect existing IDs (more reliable than repeated guessing)
    existing_ids = set()

    # If inventory supports iteration (BST/dict-like)
    try:
        existing_ids = set(inventory.keys())
    except:
        # fallback: try manual scan if needed
        pass

    available_ids = list(set(range(111, 10000)) - existing_ids)

    if not available_ids:
        print("No available IDs left to generate medicines.")
        return

    count = 0

    for _ in range(n):
        if not available_ids:
            print("Ran out of unique IDs while generating.")
            break

        medicine_id = random.choice(available_ids)
        available_ids.remove(medicine_id)

        name = f"Medicine {medicine_id}"
        category = random.choice(["Tablet", "Syrup", "Supplement", "Capsule"])
        price = round(random.uniform(2.0, 150.0), 2)
        stock = random.randint(1, 200)

        new_medicine = Medicine(medicine_id, name, category, price, stock)

        inventory.insertNode(medicine_id, new_medicine)
        medicine_list.append(new_medicine)

        count += 1

    print(f"{count} random medicines added successfully!")

def main():
    while True:
        try:
            capacity = int(input("Enter hash table capacity (minimum 10): "))
            if capacity < 10:
                print("Capacity must be at least 10.")
            else:
                break
        except ValueError:
            print("Please enter a valid number.")

    inventory = hashMap(capacity)
    # Pre-defined pharmacy products
    predefined_products = [
        Medicine(101, "Panadol", "Tablet", 8.50, 100),
        Medicine(102, "Cough Syrup", "Syrup", 12.90, 50),
        Medicine(103, "Vitamin C", "Supplement", 25.00, 75),
        Medicine(104, "Ibuprofen", "Tablet", 15.50, 80),
        Medicine(105, "Antacid", "Tablet", 9.90, 60),
        Medicine(106, "Fish Oil", "Supplement", 35.00, 40),
        Medicine(107, "Paracetamol", "Tablet", 7.50, 120),
        Medicine(108, "Multivitamin", "Supplement", 28.00, 55),
        Medicine(109, "Allergy Relief", "Tablet", 18.50, 30),
        Medicine(110, "Throat Lozenges", "Lozenge", 6.50, 90)
    ]

    array = predefined_products.copy()

    # Insert into hash table
    for medicine in predefined_products:
        inventory.insertNode(medicine.medicine_id, medicine)

    while True:
        print("\n--- Pharmacy Inventory System ---")
        print("1. Insert Medicine")
        print("2. Search Medicine")
        print("3. Edit Medicine")
        print("4. Delete Medicine")
        print("5. Display Inventory")
        print("6. Exit")
        print("7. Add Random Products")  # Optional

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            try:
                medicine_id = int(input("Enter Medicine ID: "))
                name = input("Enter Medicine Name: ").strip()
                category = input("Enter Category (Tablet/Syrup/Supplement): ").strip()
                price = float(input("Enter Price: "))
                stock = int(input("Enter Stock Quantity: "))

                new_medicine = Medicine(
                    medicine_id,
                    name,
                    category,
                    round(price, 2),
                    stock
                )

                inventory.insertNode(medicine_id, new_medicine)
                array.append(new_medicine)

                print("Medicine added successfully!")

            except ValueError:
                print("Invalid input.")

        elif choice == "2":
            try:
                search_id = int(input("Enter Medicine ID to search: "))

                # =========================
                # SEARCH IN HASH TABLE
                # =========================
                start_hash = time.perf_counter()
                result_hash = inventory.get(search_id)
                end_hash = time.perf_counter()

                if result_hash != -1:
                    print(f"\nHash Table: Medicine Found:\n{result_hash}")
                else:
                    print("\nHash Table: Medicine not found.")

                print(f"Hash Table search time: {end_hash - start_hash:.8f} seconds")

                # =========================
                # SEARCH IN ARRAY (LINEAR SEARCH)
                # =========================
                start_array = time.perf_counter()

                result_array = None
                for item in array:
                    if item.medicine_id == search_id:
                        result_array = item
                        break

                end_array = time.perf_counter()

                if result_array:
                    print(f"\nArray: Medicine Found:\n{result_array}")
                else:
                    print("\nArray: Medicine not found.")

                print(f"Array search time: {end_array - start_array:.8f} seconds")

            except ValueError:
                print("Invalid input. Please enter a numeric Medicine ID.")

        elif choice == "3":
            try:
                edit_id = int(input("Enter Medicine ID to edit: "))

                medicine = inventory.get(edit_id)

                if medicine != -1:
                    print(f"\nCurrent Record:\n{medicine}")

                    new_name = input(
                        f"Enter new name [{medicine.name}]: "
                    ).strip() or medicine.name

                    new_category = input(
                        f"Enter new category [{medicine.category}]: "
                    ).strip() or medicine.category

                    price_input = input(
                        f"Enter new price [{medicine.price}]: "
                    ).strip()

                    stock_input = input(
                        f"Enter new stock [{medicine.stock}]: "
                    ).strip()

                    medicine.name = new_name
                    medicine.category = new_category

                    if price_input:
                        medicine.price = round(float(price_input), 2)

                    if stock_input:
                        medicine.stock = int(stock_input)

                    print("Medicine updated successfully!")

                else:
                    print("Medicine not found.")

            except ValueError:
                print("Invalid input.")

        elif choice == "4":
            try:
                delete_id = int(input("Enter Medicine ID to delete: "))

                deleted = inventory.deleteNode(delete_id)

                if deleted != -1:
                    array[:] = [
                        item for item in array
                        if item.medicine_id != delete_id
                    ]
                    print("Medicine deleted successfully!")
                else:
                    print("Medicine not found.")

            except ValueError:
                print("Invalid input.")

        elif choice == "5":
            print("\n" + "=" * 40)
            print("ALL MEDICINES IN ARRAY")
            print("=" * 40)

            if not array:
                print("The inventory is empty.")
                return

            for index, item in enumerate(array, start=1):
                print(f"{index}. {item}")  # Prints the object

            print("=" * 40)
            print(f"Total items: {len(array)}\n")

            print("\n--- Pharmacy Inventory (for hash) ---")
            for node in inventory.arr:
                if node is not None and node.key != -1:
                    print(node.value)

        elif choice == "6":
            print("Exiting Pharmacy Inventory System.")
            break
        elif choice == "7":
            try:
                n = int(input("How many random products to add? "))

                available_space = inventory.capacity - inventory.size

                if n <= 0:
                    print("Please enter a number greater than 0.")

                elif n > available_space:
                    print(
                        f"Cannot add {n} items. Only {available_space} slots available (out of {inventory.capacity}).")

                else:
                    add_random_medicines(inventory, array, n)

            except ValueError:
                print("Invalid input. Please enter a number.")

        else:
            print("Invalid choice.")



if __name__ == "__main__":
    main()