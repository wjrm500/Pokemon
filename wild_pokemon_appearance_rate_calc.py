from pokemon_stat_calc import StatCalculator
from pokemon_csv import base_stats
import pandas as pd
from funcs import inclusive_range
import numpy as np

frames = []
global_ivs = {stat: 15 for stat in ["hp", "attack", "defense", "sp_attack", "sp_defense", "speed"]}
for i in range(386):
    d = {}
    species = base_stats.index[i]
    bs = base_stats.iloc[i].to_dict()
    for j in inclusive_range(1, 100):
        stats = StatCalculator(level = j, ivs = global_ivs, nature = "Bashful", base_stats = bs)
        total_stat = int(np.sum(list(stats.values())))
        d[i * j] = {
            "species": species,
            "level": j,
            "total_stat": total_stat
        }
    f = pd.DataFrame.from_dict(d).transpose()
    frames.append(f)

a = pd.concat(frames)
