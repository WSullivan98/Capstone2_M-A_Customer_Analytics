import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns 
from operator import attrgetter
import warnings









if __name__ == "__main__":
    data = pd.read_csv('../data/processed/sales.csv')
    print(data.head())