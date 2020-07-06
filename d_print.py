"""
Print calculated results
"""

# Decemal places
DP = 6

class Print:

    @staticmethod
    def features(data, terminal_width, i):
        # Length of the word "Count"
        printed = 5
        print(f"{'':<{printed}}", end="")
        while i < data.features_nb and printed + data.width[i] <= terminal_width:
            print(f"{data.features[i]:>{data.width[i]}}", end="")
            printed += data.width[i]
            i += 1

    @staticmethod
    def calculations(data, terminal_width, start):
        for key in ("Count", "Mean", "Std", "Min", "25%", "50%", "75%", "Max"):
            printed = 5
            print(f"\n{key:<{printed}}", end="")
            i = start
            while i < data.features_nb and printed + data.width[i] <= terminal_width:
                if key == "Count" and "Max" not in data.info[i]:
                    print(f"{data.info[i][key]:>{data.width[i]}}", end="")
                elif key in data.info[i]:
                    print(f"{data.info[i][key]:>{data.width[i]}.{DP}f}", end="")
                else:
                    print(f"{'NaN':>{data.width[i]}}", end="")
                printed += data.width[i]
                i += 1
        return i