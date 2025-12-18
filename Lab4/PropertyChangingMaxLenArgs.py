from typing import Any


class PropertyChangingMaxLenArgs:
    def __init__(self, prop_name: str, old_value: Any, new_value: Any, min_len: int, max_len: int) -> None:
        self.prop_name = prop_name
        self.old_value = old_value
        self.new_value = new_value
        self.min_len = min_len
        self.max_len = max_len
