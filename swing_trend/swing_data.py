import copy
from swing_trend.node_class import Node


class CandleLinkList:
    def __init__(self, series):
        self.nodes = []
        self.length = len(series)
        self.windowRatio = 0.005
        self.processHighLows(series)

    def al_sat_mod_hesapla(self, tahmin):
        # son low en dusugu bi onceki low'un en dusugunden yuksek ise ETH al
        # son high bi onceki high'in en yukseginden dusukse ETH sat
        son_low = self.lowNodes[0]
        bionceki_low = self.lowNodes[1]
        son_high = self.highNodes[0]
        bionceki_high = self.highNodes[1]
        upperP = tahmin[1]
        lowerP = tahmin[2]
        openP = tahmin[3]
        self.karar = None
        if son_low.low > bionceki_low.low:
            self.karar = 'al'
        elif son_high.high < bionceki_high.high:
            self.karar = 'sat'
        elif openP < lowerP:
            self.karar = 'sat'
        elif openP > upperP:
            self.karar = 'al'
        return self.karar

    def processHighLows(self, series):
        self.createNodes(series)
        self.markMinors()
        self.markMajors(self)
        # self.majorsTrend()

    def createNodes(self, series):
        self.nodes = []
        for i in range(0, self.length):
            node = Node(series.iloc[i], i, self.nodes)
            self.nodes.append(node)

    def markMinors(self):
        self.highNodes = []
        self.lowNodes = []
        for node in self.nodes:
            node.calculateMinors()
            # highCopy = copy.deepcopy(node)
            # lowCopy = copy.deepcopy(node)

            if node.isHigh:
                self.highNodes.append(node)
            if node.isLow:
                self.lowNodes.append(node)
        self.connectNodes(self.highNodes)
        self.connectNodes(self.lowNodes)

    def markMajors(self, that):
        self.lastMajorHigh = None
        self.lastMajorLow = None
        self.prevMajorHigh = None
        self.prevMajorLow = None
        self.majorHighs = []
        self.majorLows = []
        for i in range(0, len(self.highNodes)):
        # while i >= 0:
            node = self.highNodes[i]
            node.calculateMajors("high", that)
            if node.isMajorHigh:
                self.majorHighs.append(node)

        for k in range(0, len(self.lowNodes)):
        # while k >= 0:
            node = self.lowNodes[k]
            node.calculateMajors("low", that)
            if node.isMajorLow:
                self.majorLows.append(node)

    @staticmethod
    def connectNodes(nodeList):
        _len = len(nodeList)
        for i in range(0, _len):
            prev2nd = nodeList[i + 2] if i < _len - 2 else None
            next2nd = nodeList[i - 2] if i - 2 >= 0 else None
            nodeList[i].prev2nd = prev2nd
            nodeList[i].next2nd = next2nd
            next = nodeList[i - 1] if i - 1 >= 0 else None
            prev = nodeList[i + 1] if i < _len - 1 else None
            nodeList[i].next = next
            nodeList[i].prev = prev

