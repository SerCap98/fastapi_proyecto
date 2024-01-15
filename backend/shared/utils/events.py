from datetime import date
from uuid import UUID

from modules.users.users.user_schemas import UserInDB


class InventoryUpdatedEvent:
    def __init__(self, inventory_id: UUID, new_quantity: float, min_quantity: float, current_user:UserInDB):
        self.inventory_id = inventory_id
        self.new_quantity = new_quantity
        self.min_quantity = min_quantity
        self.current_user = current_user

class FormulaUpdatedEvent:
    def __init__(self, formula_id: UUID, new_quantity: float, current_user:UserInDB):
        self.formula_id = formula_id
        self.new_quantity = new_quantity
        self.current_user = current_user

class OrderUpdatedEvent:
    def __init__(self, order_id: UUID, new_quantity: float, client: str, total_cost: float, note: str, discount: int, delivered: bool, date_delivered: date, current_user:UserInDB):
        self.order_id = order_id
        self.new_quantity = new_quantity
        self.client = client
        self.total_cost = total_cost
        self.note = note
        self.discount = discount
        self.delivered = delivered
        self.date_delivered = date_delivered
        self.current_user = current_user

class EventBus:
    subscribers = {}

    @classmethod
    def subscribe(cls, event_type, handler):
        cls.subscribers.setdefault(event_type, []).append(handler)


    @classmethod
    async def publish(cls, event):
 
        for handler in cls.subscribers.get(type(event), []):

            await handler(event)