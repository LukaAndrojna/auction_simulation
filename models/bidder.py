from typing import List
from random import uniform


class SimpleBidder:
    def __init__(self, tv: float):
        self._true_value = tv
        self._highest_bid = tv
        self._lowest_bid = 0
        self._bids = list()
    
    def get_bid(self) -> float:
        self._bids.append(round(uniform(self._lowest_bid, self._highest_bid), 2))
        return self._bids[-1]

    
    def update(self, bid: float, won: bool):
        if won:
            self._highest_bid = bid
        else:
            self._highest_bid = self._true_value
            self._lowest_bid = min(bid + 0.01, self._true_value)
    
    def get_bidding(self) -> List:
        return self._bids
    
    def reset(self):
        self._highest_bid = self._true_value
        self._lowest_bid = 0
        self._bids = list()