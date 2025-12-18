class PropertyChangedEventArgs:
    def __init__(self, prop_name: str) -> None:
        self.prop_name = prop_name
