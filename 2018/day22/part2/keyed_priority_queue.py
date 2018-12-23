from operator import attrgetter

class Item:
    def __init__(self, key, value, priority=None):
        self.key = key
        self.value = value
        self.priority = priority

class KeyedPriorityQueue:
    def __init__(self):
        self.keyed_items = {}
        self.sorted_items = []

    def empty(self):
        return not self.sorted_items

    def get(self, key, default):
        return self.keyed_items.get(key, Item(key, default)).value

    def insert(self, key, value, priority):
        if key in self.keyed_items:
            self.keyed_items[key].value = value
            self.keyed_items[key].priority = priority
        else:
            new_item = Item(key, value, priority)
            self.keyed_items[key] = new_item 
            self.sorted_items.append(new_item)
        self.sorted_items = sorted(self.sorted_items,
            key=attrgetter("priority"), reverse=True)

    def pop(self):
        item = self.sorted_items.pop()
        del self.keyed_items[item.key]
        return item.value

