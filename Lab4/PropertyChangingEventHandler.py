from EventHandler import EventHandler
from PropertyChangingEventArgs import PropertyChangingEventArgs
from typing import Generic, TypeVar

TEventArgs = TypeVar("TEventArgs")


class PropertyChangingEventHandler(Generic[TEventArgs], EventHandler[PropertyChangingEventArgs]):
    def handle(self, sender: object, args: PropertyChangingEventArgs) -> None:
        if isinstance(args, PropertyChangingEventArgs):
            if not args.can_change:
                sender.__dict__[args.prop_name] = args.old_value
                print(f'Changing property {args.prop_name} in object {sender} from {args.old_value} to {args.new_value} was cancelled')
                return

            print(f'Property {args.prop_name} in object {sender} was changed from {args.old_value} to {args.new_value}')
