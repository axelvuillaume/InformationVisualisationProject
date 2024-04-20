from utils import data_processing as dp

columns = ["price", "dlc_count", "positive", "negative", "average_playtime_forever", "median_playtime_forever", "peak_ccu", "min_owners", "max_owners"]
per_things = ["categories", "full_audio_languages", "genres", "supported_languages"]

dp.make_percentage_files(columns, per_things)