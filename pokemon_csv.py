import pandas as pd
from tabulate import tabulate

df = pd.read_csv("pokemon_data.csv")
df = df.head(150)
df.rename(columns = {"name": "species"}, inplace = True)
df = df.astype({"capture_rate": "int64"})

base_stats = df[["species", "hp", "attack", "defense", "sp_attack", "sp_defense", "speed"]]
base_stats.set_index("species", inplace = True)

against_cols = list(range(1, 19))
against_cols.insert(0, df.columns.get_loc("species"))
resistances = df.iloc[:, against_cols]
resistances.set_index("species", inplace = True)

exp_mapping = {
    800_000: "fast",
    1_000_000: "medium_fast",
    1_059_860: "medium_slow",
    1_250_000: "slow"
    }

df["growth_pattern"] = df["experience_growth"].map(exp_mapping)
growth_patterns = df[["species", "growth_pattern"]]
growth_patterns.set_index("species", inplace = True)

exp_by_level = pd.read_csv("pokemon_exp.csv")
exp_by_level.set_index("level", inplace = True)

capture_rates = df[["species", "capture_rate"]]
capture_rates.set_index("species", inplace = True)

natures = pd.read_csv("pokemon_nature.csv")
natures.set_index("nature", inplace = True)

moves = pd.read_csv("pokemon_moves.csv")
moves.set_index("Name", inplace = True)
