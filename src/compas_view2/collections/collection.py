from compas.data import Data
from typing import Tuple, Union, List


class Collection:
    """A collection of COMPAS items like meshes or shapes."""

    def __init__(self, items: Union[Data, Tuple[Data, dict]] = None, item_properties: List[dict] = None):
        super().__init__()
        self.items = []
        self.item_properties = []
        items = items or []
        item_properties = item_properties or []
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
