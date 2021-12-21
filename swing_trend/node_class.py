class SimpleNode:
    def __init__(self, candle, i):
        self.index = i
        self.Open_Time = candle.get("Open Time")
        self.open = candle.get("Open")
        self.high = candle.get("High")
        self.low = candle.get("Low")
        self.close = candle.get("Close")


class Node(SimpleNode):
    def __init__(self, element, index, nodes):
        super().__init__(element, index)
        self.isHigh = False
        self.isLow = False
        self.isMajorHigh = False
        self.isMajorLow = False
        self.next = None
        self.next2nd = None
        self.prev = None
        self.prev2nd = None
        self.connect(nodes)

    def connect(self, nodes):
        try:
            next = nodes[self.index - 1]
            self.next = next
            next.prev = self
        except IndexError:
            print("ilk node isleme devam...")

        try:
            next2nd = nodes[self.index - 2]
            next2nd.prev2nd = self
            self.next2nd = next2nd
        except IndexError:
            print("ikinci node isleme devam...")

    def calculateMajors(self, _type, that):
        if _type == 'high':
            self.isMajorHigh = self._isMajorHigh()
            if self.isMajorHigh and not that.lastMajorHigh:
                that.lastMajorHigh = self
                return
            if self.isMajorHigh and not that.prevMajorHigh:
                that.prevMajorHigh = self
                return
        elif _type == 'low':
            self.isMajorLow = self._isMajorLow()
            if self.isMajorLow and not that.lastMajorLow:
                that.lastMajorLow = self
                return

            if self.isMajorLow and not that.prevMajorLow:
                that.prevMajorLow = self
                return
        else:
            raise Exception("Wrong calculate type entered!")

    def calculateMinors(self):
        self.isHigh = self._isHigh()
        self.isLow = self._isLow()
        self.isGreen = self._isGreen()
        self.isRed = self._isRed()

    def _isMajorHigh(self):
        resistance = False
        if not self.prev or not self.prev2nd:
            return resistance

        if self.next and self.next2nd:
            resistance = self.high >= self.prev.high and self.high >= self.next.high \
                         and self.high >= self.next2nd.high and self.high >= self.prev2nd.high

        elif self.next and not self.next2nd:
            resistance = self.high >= self.prev.high and self.high >= self.next.high \
                         and self.high >= self.prev2nd.high
        elif not self.next and not self.next2nd:
            resistance = self.high >= self.prev.high and self.high >= self.prev2nd.high

        return resistance

    def _isMajorLow(self):
        support = False
        if not self.prev or not self.prev2nd:
            return support

        if self.next and self.next2nd:
            support = self.low <= self.prev.low and self.low <= self.next.low \
                      and self.low <= self.next2nd.low and self.low <= self.prev2nd.low
        elif self.next and not self.next2nd:
            support = self.low <= self.prev.low and self.low <= self.next.low \
                      and self.low <= self.prev2nd.low
        elif not self.next and not self.next2nd:
            support = self.low <= self.prev.low and self.low <= self.prev2nd.low

        return support

    def _isGreen(self):
        if self.close > self.open:
            return True
        return False

    def _isRed(self):
        if self.open > self.close:
            return True
        return False

    def _isLow(self):
        support = False
        if not self.prev or not self.prev2nd:
            return support

        if self.next and self.next2nd:
            support = self.low <= self.prev.low and self.low <= self.next.low\
            and self.low <= self.next2nd.low and self.low <= self.prev2nd.low

        return support

    def _isHigh(self):
        resistance = False
        if not self.prev or not self.prev2nd:
            return resistance

        if self.next and self.next2nd:
            resistance = self.high >= self.prev.high and self.high >= self.next.high\
            and self.high >= self.next2nd.high and self.high >= self.prev2nd.high

        return resistance

