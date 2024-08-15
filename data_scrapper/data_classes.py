from dataclasses import dataclass, field

@dataclass
class ShareVal:
    name: str
    open: float
    high: float
    low: float
    prev_close: float
    ltp: float
    change: float
    volume: float
    value: float
    tc: float = 0.0
    pivot: float = 0.0
    bc: float = 0.0
    res_1: float = 0.0
    res_2: float = 0.0
    res_3: float = 0.0
    res_4: float = 0.0
    sup_1: float = 0.0
    sup_2: float = 0.0
    sup_3: float = 0.0
    sup_4: float = 0.0

    def __post_init__(self):
        self.open = float(self.open)
        self.high = float(self.high)
        self.low = float(self.low)
        self.prev_close = float(self.prev_close)
        self.ltp = float(self.ltp)
        self.value = float(self.value)

        self.pivot = (self.high + self.low + self.ltp) / 3
        self.bc = (self.high + self.low) / 2
        self.tc = 2 * self.pivot - self.bc

        self.res_1 = 2 * self.pivot - self.low
        self.res_2 = self.pivot + self.high - self.low
        self.res_3 = self.res_1 + self.high - self.low
        self.res_4 = self.res_3 + self.res_2 - self.res_1

        self.sup_1 = 2 * self.pivot - self.high
        self.sup_2 = self.pivot - self.high + self.low
        self.sup_3 = self.sup_1 - self.high + self.low
        self.sup_4 = self.sup_3 - self.sup_1 + self.sup_2


@dataclass
class ShareAttributes:
    share_info: list = field(default_factory=list)
