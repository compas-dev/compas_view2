from compas.data import Data
from typing import Tuple, Union, List


class Collection:
    """A collection of COMPAS items like meshes or shapes.
    """

    def __init__(self, items: Union[Data, Tuple[Data, dict]], item_properties: List[dict] = None):
        super().__init__()
        self.items = []
        self.item_properties = []
        for item in items:
            if isinstance(item, Data):
                self.item_properties.append({})
            else:
                item, properties = item
                self.item_properties.append(properties)
            self.items.append(item)

        if item_properties:
            self.item_properties = item_properties

        assert len(self.items) == len(self.item_properties)

    @property    
    def is_vector(self):
        return isinstance(self.items[0], Vector)
