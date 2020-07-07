"""
Print calculated results
"""

# Length of the word "Count"
PRINTED = 5
# Decemal places
DP = 6

class Print:

    @staticmethod
    def features(data, features, terminal_width, i):
        printed = PRINTED
        print(f"{'':<{printed}}", end="")
        while i < features.nb and printed + features.width[i] <= terminal_width:
            print(f"{features.titles[i]:>{features.width[i]}}", end="")
            printed += features.width[i]
            i += 1

    @staticmethod
    def calculations(data, features, terminal_width, start):
        for key in ("Count", "Mean", "Std", "Min", "25%", "50%", "75%", "Max"):
            printed = PRINTED
            print(f"\n{key:<{printed}}", end="")
            i = start
            while i < features.nb and printed + features.width[i] <= terminal_width:
                if key == "Count" and "Max" not in data.info[i]:
                    print(f"{data.info[i][key]:>{features.width[i]}}", end="")
                elif key in data.info[i]:
                    print(f"{data.info[i][key]:>{features.width[i]}.{DP}f}", end="")
                else:
                    print(f"{'NaN':>{features.width[i]}}", end="")
                printed += features.width[i]
                i += 1
        return i