def StatCalculator(level, ivs, nature, base_stats):
    from pokemon_csv import natures
    import numpy as np
    import pandas as pd

    non_hp_base_stats = base_stats
    hp_base_stat = non_hp_base_stats.pop("hp")
    non_hp_ivs = ivs
    hp_iv = non_hp_ivs.pop("hp")

    hp_stat = {"hp": np.floor((2 * hp_base_stat + hp_iv) * level / 100 + level + 10)}
    non_hp_stats = {i: np.floor((2 * non_hp_base_stats[i] + non_hp_ivs[i]) * level / 100 + 5) for i in non_hp_base_stats}

    increased_stat = natures.loc[nature].increase
    if pd.notnull(increased_stat):
        non_hp_stats[increased_stat] = np.floor(non_hp_stats[increased_stat] * 1.1)
    decreased_stat = natures.loc[nature].decrease
    if pd.notnull(decreased_stat):
        non_hp_stats[decreased_stat] = np.floor(non_hp_stats[decreased_stat] * 0.9)

    all_stats = {}
    all_stats.update(hp_stat)
    all_stats.update(non_hp_stats)

    return all_stats
