import os
import shutil

def move_issues(root, issues, suffix, dir_number, report):
    if len(issues) == 1:
        return
    if suffix == "F":
        new_directory = os.path.join(root, "false")
    else:
        new_directory = os.path.join(root, f"{dir_number:03d}-{suffix}")

    os.makedirs(new_directory, exist_ok=True)

    for issue in issues:
        issue_filename = f"{issue:03d}.md"
        if issue == report:
            report_filename = f"{issue:03d}-best.md"
            os.rename(
                os.path.join(root, issue_filename), os.path.join(root, report_filename)
            )
            issue_filename = report_filename
        shutil.move(os.path.join(root, issue_filename), new_directory)

families = [{'severity': 'high', 'report': 102, 'issues': [18, 19, 102, 180, 281]}, {'severity': 'high', 'report': 125, 'issues': [11, 37, 125, 160]}, {'severity': 'high', 'report': 63, 'issues': [63, 159, 215]}, {'severity': 'high', 'report': 114, 'issues': [108, 114]}, {'severity': 'medium', 'report': 105, 'issues': [67, 105, 163, 202]}, {'severity': 'high', 'report': 112, 'issues': [22, 112, 265]}, {'severity': 'medium', 'report': 109, 'issues': [109, 224, 266]}, {'severity': 'medium', 'report': 13, 'issues': [13, 93]}, {'severity': 'medium', 'report': 295, 'issues': [36, 295]}, {'severity': 'high', 'report': 115, 'issues': [69, 115]}, {'severity': 'medium', 'report': 72, 'issues': [72, 107]}, {'severity': 'high', 'report': 94, 'issues': [94, 248]}, {'severity': 'medium', 'report': 113, 'issues': [113, 282]}, {'severity': 'medium', 'report': 187, 'issues': [187, 231]}, {'severity': 'medium', 'report': 95, 'issues': [86, 95, 161, 173, 254, 275]}, {'severity': 'medium', 'report': 162, 'issues': [73, 162]}, {'severity': 'medium', 'report': 100, 'issues': [100, 276]}, {'severity': 'medium', 'report': 17, 'issues': [14, 17]}, {'severity': 'high', 'report': 26, 'issues': [26, 78]}, {'severity': 'medium', 'report': 117, 'issues': [54, 117]}, {'severity': 'medium', 'report': 59, 'issues': [59]}, {'severity': 'medium', 'report': 135, 'issues': [135]}, {'severity': 'medium', 'report': 44, 'issues': [44]}, {'severity': 'medium', 'report': 230, 'issues': [230]}, {'severity': 'medium', 'report': 250, 'issues': [250]}, {'severity': 'medium', 'report': 251, 'issues': [251]}, {'severity': 'high', 'report': 15, 'issues': [15]}, {'severity': 'high', 'report': 96, 'issues': [96]}, {'severity': 'high', 'report': 165, 'issues': [165]}, {'severity': 'medium', 'report': 124, 'issues': [124]}, {'severity': 'medium', 'report': 170, 'issues': [170]}, {'severity': 'medium', 'report': 272, 'issues': [272]}, {'severity': 'medium', 'report': 28, 'issues': [28]}, {'severity': 'medium', 'report': 203, 'issues': [203]}, {'severity': 'high', 'report': 110, 'issues': [110]}, {'severity': 'high', 'report': 116, 'issues': [116]}, {'severity': 'medium', 'report': 118, 'issues': [118]}, {'severity': 'medium', 'report': 207, 'issues': [207]}, {'severity': 'medium', 'report': 183, 'issues': [183]}, {'severity': 'medium', 'report': 311, 'issues': [311]}, {'severity': 'medium', 'report': 21, 'issues': [21]}, {'severity': 'medium', 'report': 262, 'issues': [262]}, {'severity': 'medium', 'report': 20, 'issues': [20]}, {'severity': 'medium', 'report': 87, 'issues': [87]}, {'severity': 'medium', 'report': 148, 'issues': [148]}, {'severity': 'medium', 'report': 129, 'issues': [129]}, {'severity': 'medium', 'report': 247, 'issues': [247]}, {'severity': 'medium', 'report': 260, 'issues': [260]}, {'severity': 'medium', 'report': 39, 'issues': [39]}, {'severity': 'medium', 'report': 64, 'issues': [64]}, {'severity': 'medium', 'report': 65, 'issues': [65]}, {'severity': 'medium', 'report': 74, 'issues': [74]}, {'severity': 'medium', 'report': 12, 'issues': [12]}, {'severity': 'medium', 'report': 218, 'issues': [218]}, {'severity': 'medium', 'report': 292, 'issues': [292]}, {'severity': 'medium', 'report': 91, 'issues': [91]}, {'severity': 'medium', 'report': 264, 'issues': [264]}, {'severity': 'medium', 'report': 293, 'issues': [293]}, {'severity': 'medium', 'report': 51, 'issues': [51]}, {'severity': 'medium', 'report': 220, 'issues': [220]}, {'severity': 'medium', 'report': 68, 'issues': [68]}, {'severity': 'medium', 'report': 227, 'issues': [227]}, {'severity': 'medium', 'report': 123, 'issues': [123]}, {'severity': 'medium', 'report': 184, 'issues': [184]}, {'severity': 'medium', 'report': 192, 'issues': [192]}, {'severity': 'medium', 'report': 306, 'issues': [306]}, {'severity': 'medium', 'report': 287, 'issues': [287]}, {'severity': 'medium', 'report': 305, 'issues': [305]}, {'severity': 'medium', 'report': 98, 'issues': [98]}, {'severity': 'medium', 'report': 255, 'issues': [255]}, {'severity': 'medium', 'report': 179, 'issues': [179]}, {'severity': 'medium', 'report': 238, 'issues': [238]}, {'severity': 'medium', 'report': 27, 'issues': [27]}, {'severity': 'medium', 'report': 40, 'issues': [40]}, {'severity': 'medium', 'report': 66, 'issues': [66]}, {'severity': 'medium', 'report': 82, 'issues': [82]}, {'severity': 'high', 'report': 119, 'issues': [119]}, {'severity': 'high', 'report': 126, 'issues': [126]}, {'severity': 'medium', 'report': 47, 'issues': [47]}, {'severity': 'medium', 'report': 303, 'issues': [303]}, {'severity': 'medium', 'report': 75, 'issues': [75]}, {'severity': 'medium', 'report': 261, 'issues': [261]}, {'severity': 'medium', 'report': 141, 'issues': [141]}, {'severity': 'medium', 'report': 217, 'issues': [217]}, {'severity': 'medium', 'report': 157, 'issues': [157]}, {'severity': 'medium', 'report': 166, 'issues': [166]}, {'severity': 'medium', 'report': 167, 'issues': [167]}, {'severity': 'medium', 'report': 232, 'issues': [232]}, {'severity': 'medium', 'report': 249, 'issues': [249]}, {'severity': 'medium', 'report': 308, 'issues': [308]}, {'severity': 'medium', 'report': 307, 'issues': [307]}, {'severity': 'medium', 'report': 322, 'issues': [322]}, {'severity': 'medium', 'report': 33, 'issues': [33]}, {'severity': 'medium', 'report': 158, 'issues': [158]}, {'severity': 'medium', 'report': 185, 'issues': [185]}, {'severity': 'medium', 'report': 297, 'issues': [297]}, {'severity': 'medium', 'report': 25, 'issues': [25]}, {'severity': 'medium', 'report': 237, 'issues': [237]}, {'severity': 'medium', 'report': 35, 'issues': [35]}, {'severity': 'medium', 'report': 280, 'issues': [280]}, {'severity': 'medium', 'report': 62, 'issues': [62]}, {'severity': 'medium', 'report': 140, 'issues': [140]}, {'severity': 'medium', 'report': 146, 'issues': [146]}, {'severity': 'medium', 'report': 198, 'issues': [198]}, {'severity': 'medium', 'report': 206, 'issues': [206]}, {'severity': 'medium', 'report': 235, 'issues': [235]}, {'severity': 'medium', 'report': 210, 'issues': [210]}, {'severity': 'medium', 'report': 212, 'issues': [212]}, {'severity': 'medium', 'report': 2, 'issues': [2]}, {'severity': 'medium', 'report': 85, 'issues': [85]}, {'severity': 'medium', 'report': 31, 'issues': [31]}, {'severity': 'medium', 'report': 45, 'issues': [45]}, {'severity': 'medium', 'report': 34, 'issues': [34]}, {'severity': 'medium', 'report': 121, 'issues': [121]}, {'severity': 'medium', 'report': 143, 'issues': [143]}, {'severity': 'medium', 'report': 226, 'issues': [226]}, {'severity': 'medium', 'report': 30, 'issues': [30]}, {'severity': 'medium', 'report': 49, 'issues': [49]}, {'severity': 'medium', 'report': 32, 'issues': [32]}, {'severity': 'medium', 'report': 60, 'issues': [60]}, {'severity': 'medium', 'report': 131, 'issues': [131]}, {'severity': 'medium', 'report': 136, 'issues': [136]}, {'severity': 'medium', 'report': 240, 'issues': [240]}, {'severity': 'medium', 'report': 304, 'issues': [304]}, {'severity': 'medium', 'report': 52, 'issues': [52]}, {'severity': 'medium', 'report': 103, 'issues': [103]}, {'severity': 'medium', 'report': 139, 'issues': [139]}, {'severity': 'medium', 'report': 156, 'issues': [156]}, {'severity': 'medium', 'report': 182, 'issues': [182]}, {'severity': 'medium', 'report': 186, 'issues': [186]}, {'severity': 'medium', 'report': 222, 'issues': [222]}, {'severity': 'medium', 'report': 243, 'issues': [243]}, {'severity': 'medium', 'report': 246, 'issues': [246]}, {'severity': 'medium', 'report': 277, 'issues': [277]}, {'severity': 'medium', 'report': 61, 'issues': [61]}, {'severity': 'medium', 'report': 318, 'issues': [318]}, {'severity': 'medium', 'report': 236, 'issues': [236]}, {'severity': 'medium', 'report': 279, 'issues': [279]}, {'severity': 'medium', 'report': 6, 'issues': [6]}, {'severity': 'medium', 'report': 23, 'issues': [23]}, {'severity': 'medium', 'report': 29, 'issues': [29]}, {'severity': 'medium', 'report': 256, 'issues': [256]}, {'severity': 'medium', 'report': 43, 'issues': [43]}, {'severity': 'medium', 'report': 48, 'issues': [48]}, {'severity': 'medium', 'report': 55, 'issues': [55]}, {'severity': 'medium', 'report': 147, 'issues': [147]}, {'severity': 'medium', 'report': 214, 'issues': [214]}, {'severity': 'medium', 'report': 288, 'issues': [288]}, {'severity': 'medium', 'report': 286, 'issues': [286]}, {'severity': 'medium', 'report': 309, 'issues': [309]}, {'severity': 'medium', 'report': 4, 'issues': [4]}, {'severity': 'medium', 'report': 104, 'issues': [104]}, {'severity': 'medium', 'report': 7, 'issues': [7]}, {'severity': 'medium', 'report': 24, 'issues': [24]}, {'severity': 'medium', 'report': 16, 'issues': [16]}, {'severity': 'medium', 'report': 84, 'issues': [84]}, {'severity': 'medium', 'report': 76, 'issues': [76]}, {'severity': 'medium', 'report': 89, 'issues': [89]}, {'severity': 'medium', 'report': 122, 'issues': [122]}, {'severity': 'medium', 'report': 145, 'issues': [145]}, {'severity': 'medium', 'report': 127, 'issues': [127]}, {'severity': 'medium', 'report': 128, 'issues': [128]}, {'severity': 'medium', 'report': 151, 'issues': [151]}, {'severity': 'medium', 'report': 300, 'issues': [300]}, {'severity': 'medium', 'report': 211, 'issues': [211]}, {'severity': 'medium', 'report': 325, 'issues': [325]}, {'severity': 'medium', 'report': 1, 'issues': [1]}, {'severity': 'medium', 'report': 3, 'issues': [3]}, {'severity': 'medium', 'report': 5, 'issues': [5]}, {'severity': 'medium', 'report': 8, 'issues': [8]}, {'severity': 'medium', 'report': 9, 'issues': [9]}, {'severity': 'medium', 'report': 10, 'issues': [10]}, {'severity': 'medium', 'report': 38, 'issues': [38]}, {'severity': 'medium', 'report': 41, 'issues': [41]}, {'severity': 'medium', 'report': 42, 'issues': [42]}, {'severity': 'medium', 'report': 46, 'issues': [46]}, {'severity': 'medium', 'report': 50, 'issues': [50]}, {'severity': 'medium', 'report': 56, 'issues': [56]}, {'severity': 'medium', 'report': 57, 'issues': [57]}, {'severity': 'medium', 'report': 58, 'issues': [58]}, {'severity': 'medium', 'report': 70, 'issues': [70]}, {'severity': 'medium', 'report': 71, 'issues': [71]}, {'severity': 'medium', 'report': 77, 'issues': [77]}, {'severity': 'medium', 'report': 80, 'issues': [80]}, {'severity': 'medium', 'report': 81, 'issues': [81]}, {'severity': 'medium', 'report': 83, 'issues': [83]}, {'severity': 'medium', 'report': 90, 'issues': [90]}, {'severity': 'medium', 'report': 92, 'issues': [92]}, {'severity': 'medium', 'report': 97, 'issues': [97]}, {'severity': 'medium', 'report': 99, 'issues': [99]}, {'severity': 'medium', 'report': 101, 'issues': [101]}, {'severity': 'medium', 'report': 106, 'issues': [106]}, {'severity': 'high', 'report': 111, 'issues': [111]}, {'severity': 'medium', 'report': 120, 'issues': [120]}, {'severity': 'medium', 'report': 130, 'issues': [130]}, {'severity': 'medium', 'report': 133, 'issues': [133]}, {'severity': 'medium', 'report': 134, 'issues': [134]}, {'severity': 'medium', 'report': 137, 'issues': [137]}, {'severity': 'medium', 'report': 138, 'issues': [138]}, {'severity': 'medium', 'report': 142, 'issues': [142]}, {'severity': 'medium', 'report': 144, 'issues': [144]}, {'severity': 'medium', 'report': 149, 'issues': [149]}, {'severity': 'high', 'report': 150, 'issues': [150]}, {'severity': 'medium', 'report': 152, 'issues': [152]}, {'severity': 'high', 'report': 153, 'issues': [153]}, {'severity': 'high', 'report': 154, 'issues': [154]}, {'severity': 'medium', 'report': 155, 'issues': [155]}, {'severity': 'high', 'report': 164, 'issues': [164]}, {'severity': 'medium', 'report': 168, 'issues': [168]}, {'severity': 'medium', 'report': 171, 'issues': [171]}, {'severity': 'medium', 'report': 174, 'issues': [174]}, {'severity': 'medium', 'report': 177, 'issues': [177]}, {'severity': 'high', 'report': 178, 'issues': [178]}, {'severity': 'medium', 'report': 190, 'issues': [190]}, {'severity': 'medium', 'report': 191, 'issues': [191]}, {'severity': 'medium', 'report': 193, 'issues': [193]}, {'severity': 'medium', 'report': 194, 'issues': [194]}, {'severity': 'medium', 'report': 195, 'issues': [195]}, {'severity': 'medium', 'report': 197, 'issues': [197]}, {'severity': 'medium', 'report': 199, 'issues': [199]}, {'severity': 'medium', 'report': 200, 'issues': [200]}, {'severity': 'medium', 'report': 204, 'issues': [204]}, {'severity': 'medium', 'report': 209, 'issues': [209]}, {'severity': 'medium', 'report': 213, 'issues': [213]}, {'severity': 'medium', 'report': 221, 'issues': [221]}, {'severity': 'medium', 'report': 223, 'issues': [223]}, {'severity': 'medium', 'report': 225, 'issues': [225]}, {'severity': 'medium', 'report': 228, 'issues': [228]}, {'severity': 'medium', 'report': 239, 'issues': [239]}, {'severity': 'medium', 'report': 241, 'issues': [241]}, {'severity': 'medium', 'report': 242, 'issues': [242]}, {'severity': 'high', 'report': 245, 'issues': [245]}, {'severity': 'medium', 'report': 252, 'issues': [252]}, {'severity': 'medium', 'report': 253, 'issues': [253]}, {'severity': 'medium', 'report': 258, 'issues': [258]}, {'severity': 'medium', 'report': 263, 'issues': [263]}, {'severity': 'medium', 'report': 267, 'issues': [267]}, {'severity': 'medium', 'report': 268, 'issues': [268]}, {'severity': 'high', 'report': 269, 'issues': [269]}, {'severity': 'medium', 'report': 270, 'issues': [270]}, {'severity': 'medium', 'report': 271, 'issues': [271]}, {'severity': 'high', 'report': 273, 'issues': [273]}, {'severity': 'medium', 'report': 274, 'issues': [274]}, {'severity': 'medium', 'report': 283, 'issues': [283]}, {'severity': 'medium', 'report': 284, 'issues': [284]}, {'severity': 'medium', 'report': 285, 'issues': [285]}, {'severity': 'medium', 'report': 290, 'issues': [290]}, {'severity': 'medium', 'report': 294, 'issues': [294]}, {'severity': 'medium', 'report': 298, 'issues': [298]}, {'severity': 'medium', 'report': 299, 'issues': [299]}, {'severity': 'medium', 'report': 310, 'issues': [310]}, {'severity': 'medium', 'report': 312, 'issues': [312]}, {'severity': 'high', 'report': 313, 'issues': [313]}, {'severity': 'medium', 'report': 315, 'issues': [315]}, {'severity': 'medium', 'report': 316, 'issues': [316]}, {'severity': 'medium', 'report': 317, 'issues': [317]}, {'severity': 'medium', 'report': 323, 'issues': [323]}, {'severity': 'false', 'report': None, 'issues': [234, 314, 53, 79, 88, 132, 169, 172, 175, 176, 181, 188, 189, 196, 201, 205, 208, 216, 219, 229, 233, 244, 257, 259, 278, 289, 291, 296, 301, 302, 319, 320, 321, 324, 326]}]
def main():
    last_directory_number = 0

    for family in families:
        issues = family["issues"]
        suffix = family["severity"][0].upper()
        report = family["report"]

        if suffix != "F":
            last_directory_number += 1

        move_issues(".", issues, suffix, last_directory_number, report)


if __name__ == "__main__":
    main()