# lung_cancer_BOMI2_dataset
Contains Patient IDs, clinical data, samples data, cellular data and cross validation splits. use this dataset to validate and compare with our different methods


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

