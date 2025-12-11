from typing import Any

class PropertyChangingEventArgs:
    def __init__(self, prop_name: str, old_value: Any, new_value: Any, can_change: bool) -> None:
        self.prop_name = prop_name
        self.old_value = old_value
        self.new_value = new_value
        self.can_change = can_change
    
