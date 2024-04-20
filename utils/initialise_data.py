import data_processing as dp

columns = ["price", "dlc_count", "positive", "negative", "average_playtime_forever", "median_playtime_forever", "peak_ccu", "min_owners", "max_owners"]
per_things = ["categories", "full_audio_languages", "genres", "supported_languages"]

is_done = {"categories": False, "full_audio_languages": False, "genres": False, "supported_languages": False} # Please change the truth-statement as needed.

dp.make_file(columns, per_things, is_done)