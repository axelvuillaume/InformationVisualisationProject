import pandas as pd

import data_processing as dp

tobe_merged = [x for x in dp.all_datasets if x != "cleaned"]

print(tobe_merged)