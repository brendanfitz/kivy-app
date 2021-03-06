from marshmallow import Schema, fields, post_load

class PackingItem(object):

    def __init__(self, item_name, count, packed=False):
        self.item_name = str(item_name).strip()
        self.count = int(count)
        self.packed = packed
    
    def __repr__(self):
         return (f"{self.__class__.__name__}(item_name='{self.item_name}', "
                 f"count={self.count}, packed={self.packed})")

    def __str__(self):
        return f"{self.item_name:<30}{self.count:>10}{self.packed_yesno():>10}"
    
    def __len__(self):
        return self.count
    
    def __iter__(self):
        return PackingItemIterator(self.item_name, self.count, self.packed)
    
    def __eq__(self, other):
        if not isinstance(other, PackingItem):
            return False
        return self.item_name == other.item_name
    
    @property
    def packed(self):
        return self._packed

    @packed.setter
    def packed(self, i):
        if isinstance(i, bool):
            self._packed = i 
        elif isinstance(i, str):
            if i.lower() in ('yes', 'y'):
                self._packed = True
            elif i.lower() in ('no', 'n'):
                self._packed = False 
        else:
            raise ValueError("i must be True, False, 'yes', 'y', 'no' or 'n'")
        
    def packed_yesno(self):
        return 'Yes' if self.packed else 'No'
    

class PackingItemIterator:
    def __init__(self, item_name, count, packed=False):
        self._index = 0
        self._item_data = [item_name, count, packed]
    
    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._item_data):
            raise StopIteration
        else:
            item = self._item_data[self._index]
            self._index += 1
            return item

class PackingItemSchema(Schema):
    class Meta:
        ordered = True

    item_name = fields.Str()
    count = fields.Int()
    packed = fields.Bool()

    @post_load
    def make_packing_item(self, data, **kwargs):
        return PackingItem(**data)
