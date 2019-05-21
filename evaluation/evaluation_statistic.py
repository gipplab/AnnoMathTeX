import os
import numpy as np

path = "annotations"
header = "Identifier,Name,ArXiV,Wikipedia,Wikidata,WordWindow,type"
empty = ""
source_comparison_statistic = {}

source_comparison_statistic["ArXiV_rankings"] = []
source_comparison_statistic["Wikipedia_rankings"] = []
source_comparison_statistic["Wikidata_rankings"] = []
source_comparison_statistic["WordWindow_rankings"] = []

source_comparison_statistic["ArXiV_counter"] = 0
source_comparison_statistic["Wikipedia_counter"] = 0
source_comparison_statistic["Wikidata_counter"] = 0
source_comparison_statistic["WordWindow_counter"] = 0

accepted = 0
declined = 0
total = 0

# iterate over eval files in folder
for csv_file in os.listdir(path):
    if csv_file.endswith(".csv"):

        with open(path+"/"+csv_file,"r") as f:
            print('file open')
            table = f.read().splitlines()
            for line in table:
                if line != header and line != empty:

                    total += 1

                    eval = line.split(",")

                    # source rankings
                    source_comparison_statistic["ArXiV_rankings"].append(eval[2])
                    source_comparison_statistic["Wikipedia_rankings"].append(eval[3])
                    source_comparison_statistic["Wikidata_rankings"].append(eval[4])
                    source_comparison_statistic["WordWindow_rankings"].append(eval[5])

                    # source counter
                    if eval[2] != "-":
                        source_comparison_statistic["ArXiV_counter"] += 1
                    if eval[3] != "-":
                        source_comparison_statistic["Wikipedia_counter"] += 1
                    if eval[4] != "-":
                        source_comparison_statistic["Wikidata_counter"] += 1
                    if eval[5] != "-":
                        source_comparison_statistic["WordWindow_counter"] += 1

                    # accepted/declined counter
                    for result in eval[2:5]:
                        if result != "-":
                            accepted += 1
                        else:
                            declined += 1

sum = source_comparison_statistic["ArXiV_counter"]+source_comparison_statistic["Wikipedia_counter"]+source_comparison_statistic["Wikidata_counter"]+source_comparison_statistic["WordWindow_counter"]
source_comparison_statistic["ArXiV_percentage"] = np.divide(source_comparison_statistic["ArXiV_counter"],sum)
source_comparison_statistic["Wikipedia_percentage"] = np.divide(source_comparison_statistic["Wikipedia_counter"],sum)
source_comparison_statistic["Wikidata_percentage"] = np.divide(source_comparison_statistic["Wikidata_counter"],sum)
source_comparison_statistic["WordWindow_percentage"] = np.divide(source_comparison_statistic["WordWindow_counter"],sum)

source_comparison_statistic["ArXiV_avg_ranking"] = np.mean([int(x) for x in source_comparison_statistic["ArXiV_rankings"] if x != "-"])
source_comparison_statistic["Wikipedia_avg_ranking"] = np.mean([int(x) for x in source_comparison_statistic["Wikipedia_rankings"] if x != "-"])
source_comparison_statistic["Wikidata_avg_ranking"] = np.mean([int(x) for x in source_comparison_statistic["Wikidata_rankings"] if x != "-"])
source_comparison_statistic["WordWindow_avg_ranking"] = np.mean([int(x) for x in source_comparison_statistic["WordWindow_rankings"] if x != "-"])
source_comparison_statistic["mean_avg_ranking"] = np.mean([source_comparison_statistic["ArXiV_avg_ranking"],source_comparison_statistic["Wikipedia_avg_ranking"],source_comparison_statistic["Wikidata_avg_ranking"],source_comparison_statistic["WordWindow_avg_ranking"]])

source_comparison_statistic["accepted_counter"] = accepted
source_comparison_statistic["declined_counter"] = declined
source_comparison_statistic["total_counter"] = int(np.add(accepted,declined))
source_comparison_statistic["accepted_percentage"] = np.divide(accepted,np.add(accepted,declined))

print("end")