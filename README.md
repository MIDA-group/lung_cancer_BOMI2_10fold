# Lung Cancer BOMI2 Dataset

This repository contains patient-level metadata, tissue sample information, and cross-validation splits for a cohort of 298 patients with non-small cell lung cancer (NSCLC).  
Use this dataset to validate and compare with our different methods

It is intended for machine learning and computational pathology research, in particular for:

- **Binary survival prediction** (high vs. low survival)
- **Binary subtype classification**  
  - adenocarcinoma vs. squamous cell carcinoma + others
- **Binary subtype classification (restricted)**  
  - adenocarcinoma vs. squamous cell carcinoma (excluding “others”)

---

## Cohort Overview

- **Patients:** 298  
- **Tissue samples:** 500 cores (multiple cores per patient are possible)  
- **Stains:** CD4, CD8, FoxP3, CD20, PanCK, and DAPI  
- **Features:**  
  - Extracted **cell coordinates**, **marker intensities**, **cell phenotypes**, and **nuclear morphology features** (see link below)
  - **Clinical data:** survival times, censoring, tumor stage, age, sex, histological subtype

---

## Repository Structure
lung_cancer_BOMI2_dataset/  
├── binary_survival_prediction/   
│ ├── 100foldcrossvalrepeat/  
│ │ ├── split_0_train.csv  
│ │ ├── split_0_val.csv  
│ │ ├── split_0_test.csv  
│ │ └── ...  
│ ├── 10foldcrossvalrepeat/  
│ │ ├── split_0_train.csv  
│ │ └── ...  
│ ├── static_split/  
│ │ ├── train.csv  
│ │ ├── val.csv  
│ │ ├── train_val.csv  
│ │ └── test.csv  
│ ├── Clinical_data_with_labels.csv  
│ └── samples_labels.csv  
│  
├── binary_subtype_prediction/  
│ └── (same structure as above)  
│  
├── binary_subtype_prediction_ACvsSqCC/  
│ └── (same structure as above)  
│  
└── README.md  




---

## File Descriptions

### Cross-validation splits

- **100foldcrossvalrepeat/**  
  10×10 repeated cross-validation. Each `split_k_*` file contains patient IDs for **train**, **validation**, or **test** for that fold.
- **10foldcrossvalrepeat/**  
  Standard 10-fold cross-validation (single repetition).
- **static_split/**  
  Fixed data split for reproducibility:
  - `train.csv`
  - `val.csv`
  - `train_val.csv`
  - `test.csv`

### Metadata

- **Clinical_data_with_labels.csv**  
  Patient-level clinical metadata combined with labels for the prediction task.
- **samples_labels.csv**  
  Tissue-sample-level data with patient IDs and labels.

---

## Prediction Tasks

1. **Binary survival prediction**  
   Label: Above median vs. below median overall survival.

2. **Binary subtype classification (all patients)**  
   Label: adenocarcinoma vs. squamous cell carcinoma and “others”.

3. **Binary subtype classification (restricted)**  
   Label: adenocarcinoma vs. squamous cell carcinoma.  
   Patients with “others” subtype are excluded.

---

## Cell-level Features and Raw Data

Cell-level features (coordinates, marker intensities, phenotypes, and nuclear morphology) can be accessed at:

[link to zenodo]

These features can be linked to the patient and sample IDs provided in this repository.




## create_samples.py
From `raw_data/Clinical_data_max_20190329.csv` (clinical params),
and `raw_data/TIL_tissue_seg_data.txt` (core level info),
and `raw_data/BOMI_TIL_merged_cell_seg_data_feats_1.csv` (cell level info) 
and `raw_data/id_align.csv` (patient <-> core mapping),
generate, in `binary_survival_prediction`,
 `Clinical_data_with_labels.csv` (selected clinical params, and label = 'days>=median_days'),
and `samples_labels.csv` (tumor and stroma areas for each core, mapped to patient),

## split_dataset.py
From `binary_survival_prediction/Clinical_data_with_labels.csv`,
generate, in `binary_survival_prediction`,
 `10foldcrossval/` and `100foldcrossvalrepeat/`

## generate_dataset_profile_report.py
From `binary_survival_prediction/Clinical_data_with_labels.csv`,
generate `report.html` with basic stats about the dataset.

