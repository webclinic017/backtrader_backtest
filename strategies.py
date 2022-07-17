import backtrader as bt
class stop_loss(bt.Strategy):

    def __init__(self):
        self.order = None
        #Engulfing
        self.candle_signal = bt.talib.CDLENGULFING(self.data.open,self.data.high,self.data.low, self.data.close)


    def notify_order(self, order):
        with open("log.txt", "a") as file_object:
            file_object.write("{} is next at {} \n\n".format(order,len(self)))
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            self.bar_executed = len(self)
        self.order = None


    def next(self):
        with open("log.txt", "a") as file_object:
            file_object.write("{} is next at {} \n\n".format(self.data.datetime.datetime(0),len(self)))
        if self.order:
            return
        if not self.position:
            if self.candle_signal[0]== 100:
                self.order = self.buy(exectype=bt.Order.Limit,price=self.data.close - 2.5 + 0.6)
