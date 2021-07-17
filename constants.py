COMPOUND_NAMES = []
with open("compound_names.txt", "r") as f:
  for compound_name in f:
    COMPOUND_NAMES.append(compound_name.rstrip())