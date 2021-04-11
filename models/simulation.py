from random import random, uniform

import pandas as pd
import seaborn as sns
from functools import reduce
import matplotlib.pyplot as plt

from models.bidder import SimpleBidder
from models.plotting import Plotting


class Simulation:
    def __init__(self, num_auctions: int, num_bidders, min_price: float, max_price: float, num_simulations: int):
        self._auctions = range(num_auctions)
        self._num_bidders = num_bidders
        self._initial_prices = [round(uniform(min_price, max_price), 2) for _ in range(num_bidders)]
        self._bidders = [SimpleBidder(price) for price in self._initial_prices]
        self._winners = list()
        self._num_simulations = num_simulations
        self._simulation_results = list()
        self._final_result = None
    
    def reset_bidders(self):
        for bidder in self._bidders:
            bidder.reset()

    def combine_results(self):
        self._final_result = reduce(lambda x, y: x.add(y, fill_value=0), self._simulation_results) / self._num_simulations

    def plot_results(self):
        if self._final_result is not None:
            df = pd.melt(self._final_result, 'Auction', var_name='Bidder', value_name='Bid Value')
            sns.scatterplot(data=df, x='Auction', y='Bid Value', hue='Bidder')
            plt.show()

    def plot_results_gif(self):
        if self._final_result is not None:
            df = pd.melt(self._final_result, 'Auction', var_name='Bidder', value_name='Bid Value')
            p = Plotting(df, self._auctions)
            p.create_gif()
            

    def run_single(self):
        for _ in self._auctions:
            bids = list()
            i = 0
            max_bid = 0
            for bidder_idx in range(self._num_bidders):
                bids.append(self._bidders[bidder_idx].get_bid())
                if max_bid < bids[-1] or max_bid == bids[-1] and random() < 0.5:
                    i = bidder_idx
                    max_bid = bids[-1]

            self._winners.append(self._initial_prices[i])
            for bidder_idx in range(self._num_bidders):
                self._bidders[bidder_idx].update(bids[bidder_idx], i == bidder_idx)
            
        output = {'Auction': list(self._auctions)}
        for bidder_idx in range(self._num_bidders):
            output[str(self._initial_prices[bidder_idx])] = self._bidders[bidder_idx].get_bidding()
        self._simulation_results.append(pd.DataFrame(output))
    
    def run(self):
        for _ in range(self._num_simulations):
            self.run_single()
            self.reset_bidders()
        self.combine_results()
        self.plot_results_gif()