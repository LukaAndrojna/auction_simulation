import os

import imageio
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class Plotting:
    def __init__(self, df: pd.DataFrame, auctions: int):
        self._df = df
        self._auctions = auctions
        self._images = list()
        self._max_bid = df['Bid Value'].max()

    def create_plots(self):
        path = './images/'
        for i in self._auctions:
                image_path = os.path.join(path, f'{i}.png')
                ax = sns.scatterplot(data=self._df[self._df['Auction'] <= i], x='Auction', y='Bid Value', hue='Bidder', legend=False)
                ax.set(ylim=(0, self._max_bid+1), xlim=(0, len(self._auctions)))
                plt.savefig(image_path)
                self._images.append(image_path)

    def make_gif(self):
        with imageio.get_writer('animation.gif', mode='I') as writer:
            for file_name in self._images:
                image = imageio.imread(file_name)
                writer.append_data(image)
    
    def clean_up(self):
        for file_name in set(self._images):
            os.remove(file_name)

    def create_gif(self):
        self.create_plots()
        self.make_gif()
        self.clean_up()
        
