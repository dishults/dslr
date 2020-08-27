"""
Print calculated results
"""

# Length of the word "Count"
PRINTED = 5
# Decemal places
DP = 6

def __print_align(info, width):
    print(f"{info:>{width}}", end="")

def __print_align_dp(info, width):
    print(f"{info:>{width}.{DP}f}", end="")

def features(features, terminal_width, i):
    printed = PRINTED
    print(f"{'':<{printed}}", end="")
    while i < features.nb and printed + features.width[i] <= terminal_width:
        __print_align(features.titles[i], features.width[i])
        printed += features.width[i]
        i += 1

def calculations(data, features, terminal_width, start):
    for key in ("Count", "Mean", "Std", "Min", "25%", "50%", "75%", "Max"):
        printed = PRINTED
        print(f"\n{key:<{printed}}", end="")
        i = start
        while i < features.nb and printed + features.width[i] <= terminal_width:
            if key == "Count" and "Max" not in data.info[i]:
                __print_align(data.info[i][key], features.width[i])
            elif key in data.info[i]:
                __print_align_dp(data.info[i][key], features.width[i])
            else:
                __print_align('NaN', features.width[i])
            printed += features.width[i]
            i += 1
    return i