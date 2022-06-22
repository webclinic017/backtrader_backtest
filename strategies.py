import backtrader as bt
class stop_loss(bt.Strategy):

    def __init__(self):
        self.order = None
        #Engulfing
        self.candle_signal = bt.talib.CDLENGULFING(self.data.open,self.data.high,self.data.low, self.data.close)


    def notify_order(self, order): 
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            self.bar_executed = len(self)
        self.order = None

    def next(self):
        with open("log.txt", "a") as file_object:
            file_object.write("{} is next at {} \n\n".format(self.p.valid, len(self)))
        if self.order:
            return
        if not self.position:
            if self.candle_signal[0]== 100:
                self.order = self.buy(size = 1)
                o1 = self.sell(exectype=bt.Order.Stop, price=self.data.close - 2.5 + 0.6)
                o2 = self.sell(exectype=bt.Order.Limit, price=self.data.close + 2.5 + 0.6, oco=o1)