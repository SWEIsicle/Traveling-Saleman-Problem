# HashMap class to store package data and retrieve package data.
# O(N) Space Complexity; space complexity was researched using the below citation.
# ("Hash table,") (2022)
class HashMap:
    def __init__(self, initial_capacity=16):
        self.map = []
        for i in range(initial_capacity):
            self.map.append([])

    # Insert function
    # O(N) : Worst Case
    def insert(self, key, item):  # does both insert and update
        # get the bucket list where this item will go.
        bucket = hash(key) % len(self.map)
        bucket_list = self.map[bucket]

        # update key if it is already in the bucket
        for kv in bucket_list:  # O(N) CPU time
            # print (key_value)
            if kv[0] == key:
                kv[1] = item
                return True

        # if not, insert the item to the end of the bucket list
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    # Lookup function
    # O(N) : Worst Case
    def search(self, key):
        bucket = hash(key) % len(self.map)
        bucket_list = self.map[bucket]
        for pair in bucket_list:
            if key == pair[0]:
                return pair[1]
        return None  # no pair[0] matches key 0

    # Remove function
    # O(N) Worst Case
    def remove(self, key):
        slot = hash(key) % len(self.map)
        destination = self.map[slot]

        if key in destination:
            destination.remove(key)
