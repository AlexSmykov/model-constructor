def flatten_array_of_dicts(dicts: list[dict]) -> dict:
    return {k: v for d in dicts for k, v in d.items()}
