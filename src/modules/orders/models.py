from src.modules.shared.models import TimestampModel


class Order(TimestampModel, table=True):
    pass
