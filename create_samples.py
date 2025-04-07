import pandas as pd
import numpy as np
import os


#def get_TMA(s):
#    s = s[s[]]
#    s = s.replace("BOMI2_TIL_", "")
#    s = s.replace("")
    

def preprocess_samples(data):
    data = data[data["Sample Name"].map(lambda x: "Screening" not in x)].copy()
    data.loc[:,"TMA"] = data["Slide ID"].str.replace("BOMI2_TIL_", "") + "," +  data["TMA Row"].astype(str)  + "," +  data["TMA Column"].astype(str)
    data["Sample Name"] = data["Sample Name"].map(lambda x: x.replace(".im3", ""))
    return data


def filter_samples(samples, keys, cell_data):
    keys = keys[keys["Source"] == "T1"]
    keys = keys.rename(columns={"BOMI": "ID"})
    samples = samples[samples["TMA"].isin(keys["TMA"])]
    samples = samples.merge(keys[["TMA", "ID"]], on='TMA', how='left')
    samples["sample_name_simple"] = samples["Sample Name"].map(lambda x: x[:x.rfind("_")])
    samples["sample_name_simple"] = samples["sample_name_simple"].map(lambda x: x.replace("Core[1,", "["))
    
    samples = samples[samples["sample_name_simple"].isin(cell_data["Sample Name"].unique())]
    samples = samples.drop(columns=["sample_name_simple"])
    
    return samples


#patients = pd.read_csv("raw_data/Clinical_data_max_20190329.csv")
patients = pd.read_csv("raw_data/Clinical_data_AC_SqCC.csv")
samples_data = pd.read_csv("raw_data/TIL_tissue_seg_data.txt", sep="\t")
samples_data = preprocess_samples(samples_data)

cells_data = pd.read_csv("raw_data/BOMI_TIL_merged_cell_seg_data_feats_1.csv")



keys = pd.read_csv("raw_data/id_align.csv")

samples_data = filter_samples(samples_data, keys, cells_data)

patient_ids = patients["ID"]
samples_ids = samples_data["ID"]
ids = np.intersect1d(patient_ids, samples_ids)
samples_data = samples_data[samples_data["ID"].isin(ids)]
samples = {"ID": [], "sample_name": [], "total_area": [], "tumor_area": [], "stroma_area": []}


for sample in samples_data["Sample Name"].unique():
    rows = samples_data[samples_data["Sample Name"] == sample]
    ID = rows["ID"].values[0]
    samples["ID"].append(ID)
    samples["sample_name"].append(sample)
    tumor = rows[rows["Tissue Category"] == "Tumor"]
    stroma = rows[rows["Tissue Category"] == "Stroma"]
    
    stroma_area = stroma["Region Area (pixels)"].sum()
    tumor_area = tumor["Region Area (pixels)"].sum()
    if stroma_area.size == 0:
        stroma_area = 0
    else:
        stroma_area = stroma_area.sum()
    if tumor_area.size == 0:
        tumor_area = 0
    else:
        tumor_area = tumor_area.sum()
    
    total_area = tumor_area + stroma_area
    samples["total_area"].append(total_area*0.0005**2)
    samples["tumor_area"].append(tumor_area*0.0005**2)
    samples["stroma_area"].append(stroma_area*0.0005**2)


samples = pd.DataFrame(samples)

#samples.to_csv("samples.csv", index=True)


#median_survival = patients["Follow-up (days)"].median()
#patients["label"] = (patients["Follow-up (days)"] >= median_survival).astype(int)
patients["label"] = patients["Histology"].map(lambda x: 1 if x == "Adenocarcinoma" else 0)
#patients["censored"] = patients["Dead/Alive"].map(lambda x: 1 if x== "Dead" else 0)
patients.to_csv(os.path.join("binary_subtype_prediction_ACvsSqCC", "Clinical_data_with_labels.csv"), index=False)

###Use this for survival prediction
"""
median_survival = round(patients["Follow-up (days)"].median())
print(f'Label = Follow-up (days) >= {median_survival:.1f}')
patients["label"] = (patients["Follow-up (days)"] >= median_survival).astype(int)
patients["censored"] = patients["Dead/Alive"].map(lambda x: 0 if x== "Dead" else 1) #Patient is censored if alive at end of study
"""


age_thresholds=[62,66,70,75]
patients["age_group"] = patients["Age"].map(lambda x: sum(1 for t in age_thresholds if x>=t)) #AgeGroup = sum(x>=[62,66,70,75])
patients.to_csv(os.path.join("binary_survival_prediction", "Clinical_data_with_labels.csv"), index=False)
>>>>>>> 75b9e0ed7f9133a56b479ce35d4138f35536a6d9

#patients = pd.read_csv(os.path.join("binary_survival_prediction", "Clinical_data_with_labels.csv"))

samples = samples.merge(patients[["ID", "label"]], on="ID", how="left")

samples.to_csv("binary_subtype_prediction_ACvsSqCC/samples_labels.csv", index=False)


