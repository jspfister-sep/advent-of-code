from operator import attrgetter

class Item:
    def __init__(self, key, value):
        self.key = key
        self.value = value

class KeyedPriorityQueue:
    def __init__(self):
        self.keyed_items = {}
        self.sorted_items = []

    def empty(self):
        return not self.sorted_items

    def get(self, key, default):
        return self.keyed_items.get(key, Item(key, default)).value

    def insert(self, key, value):
        if key in self.keyed_items:
            self.keyed_items[key].value = value
        else:
            new_item = Item(key, value)
            self.keyed_items[key] = new_item 
            self.sorted_items.append(new_item)
        self.sorted_items = sorted(self.sorted_items,
            key=attrgetter("value"), reverse=True)

    def pop(self):
        item = self.sorted_items.pop()
        del self.keyed_items[item.key]
        return item.value

