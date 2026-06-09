from statistics import mean

baseline = [10,12,11,9,10,11,10]
current = [19,21,18,20,22,19,21]

baseline_mean = mean(baseline)
current_mean = mean(current)

drift = abs(current_mean - baseline_mean)

print("Baseline:", baseline_mean)
print("Current:", current_mean)
print("Drift:", drift)

if drift > 5:
    print("ALERT: Significant drift detected")
