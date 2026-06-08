clean_dataset = [
    ("safe", 1),
    ("safe", 1),
    ("safe", 1),
    ("unsafe", 0)
]

poisoned_dataset = clean_dataset.copy()

poisoned_dataset.append(
    ("unsafe", 1)
)

print("Original Dataset")
print(clean_dataset)

print("\nPoisoned Dataset")
print(poisoned_dataset)

clean_positive_rate = sum(
    label
    for _, label in clean_dataset
) / len(clean_dataset)

poisoned_positive_rate = sum(
    label
    for _, label in poisoned_dataset
) / len(poisoned_dataset)

print("\nOriginal Positive Rate")
print(clean_positive_rate)

print("\nPoisoned Positive Rate")
print(poisoned_positive_rate)

print("\nImpact")

print(
    poisoned_positive_rate -
    clean_positive_rate
)
