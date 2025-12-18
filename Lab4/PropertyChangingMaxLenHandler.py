from EventHandler import EventHandler
from PropertyChangingMaxLenArgs import PropertyChangingMaxLenArgs
from typing import Generic, TypeVar

TEventArgs = TypeVar("TEventArgs")


class PropertyChangingMaxLenHandler(Generic[TEventArgs], EventHandler[PropertyChangingMaxLenArgs]):
    def handle(self, sender: object, args: PropertyChangingMaxLenArgs) -> None:
        if not isinstance(args, PropertyChangingMaxLenArgs):
            return

        if not (args.min_len <= (args.new_value if isinstance(args.new_value, (int, float)) else len(args.new_value))
                <= args.max_len):
            sender.__dict__[args.prop_name] = args.old_value
            print(f'Changing property {args.prop_name} in object {sender} from {args.old_value} to {args.new_value} was cancelled')
            return

        print(f'Property {args.prop_name} in object {sender} was changed from {args.old_value} to {args.new_value}')
