import pandas as pd

import os
from sklearn.model_selection import StratifiedKFold, train_test_split, RepeatedStratifiedKFold




def k_fold_cross_validation(df, output_dir, labelname="label", n_splits = 10):

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    
    # Initialize Stratified K-Fold
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    # Create a list to hold train-test splits
    splits = []

    # Perform stratified k-fold
    for train_index, test_index in skf.split(df, df[labelname]):
        train_val_set = df.iloc[train_index]
        test_set = df.iloc[test_index]

        train_set, val_set = train_test_split(train_val_set, 
                                           test_size=0.11, 
                                           stratify=train_val_set[labelname], 
                                           random_state=42)

        l = len(train_val_set)
        splits.append((train_set["ID"].values, test_set["ID"].values, val_set["ID"].values, train_val_set["ID"].values))


    for i, (train_set, test_set, val_set, train_val_set) in enumerate(splits):

        split_path = os.path.join(output_dir, "split_" + str(i) + ".csv")
        split = {"train": train_set, "test": test_set, "val": val_set, "train_val": train_val_set,}
        for part in split.keys():
            pd.DataFrame({"ID":split[part]}).to_csv(split_path.replace(".csv", "_" + part + ".csv"), index = False)
        


def repeated_k_fold_cross_validation(df, output_dir, labelname="label", n_splits=10, n_repeats=10):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    
    # Initialize Repeated Stratified K-Fold
    rskf = RepeatedStratifiedKFold(n_splits=n_splits, n_repeats=n_repeats, random_state=46)
    
    # Create a list to hold train-validation-test splits
    splits = []

    # Perform repeated stratified k-fold
    for repeat_index, (train_index, test_index) in enumerate(rskf.split(df, df[labelname])):
        train_val_set = df.iloc[train_index]
        test_set = df.iloc[test_index]

        train_set, val_set = train_test_split(train_val_set, 
                                               test_size=0.11, 
                                               stratify=train_val_set[labelname], 
                                               random_state=42)

        # Store the IDs for each split
        
        splits.append((repeat_index, train_set["ID"].values, test_set["ID"].values, val_set["ID"].values, train_val_set["ID"].values))

    # Save the splits to CSV files
    for repeat_index, train_set, test_set, val_set, train_val_set in splits:
        split_path = os.path.join(output_dir, f"split_{repeat_index}.csv")
        split = {
            "train": train_set,
            "test": test_set,
            "val": val_set,
            "train_val": train_val_set,
        }
        for part in split.keys():
            pd.DataFrame({"ID": split[part]}).to_csv(split_path.replace(".csv", f"_{part}.csv"), index=False)

"""
def leave_one_out_cross_validation(df, output_dir, labelname="label"):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    
    # Create a list to hold train-validation-test splits
    splits = []

    # Perform Leave-One-Out Cross-Validation
    for i in range(len(df)):
        test_set = df.iloc[[i]].reset_index(drop=True)  # Leave one observation out as the test set
        train_val_set = df.drop(i)  # Remaining observations for training and validation

        # Stratified split of the remaining training set into train and validation sets
        train_set, val_set = train_test_split(train_val_set, 
                                               test_size=0.10, 
                                               stratify=train_val_set[labelname], 
                                               random_state=42)

        # Store the IDs for each split
        splits.append((train_set["ID"].values, test_set["ID"].values, val_set["ID"].values))

    # Save the splits to CSV files
    for i, (train_set, test_set, val_set) in enumerate(splits):
        split_path = os.path.join(output_dir, f"split_{i}.csv")
        split = {
            "train": train_set,
            "test": test_set,
            "val": val_set,
        }
        for part in split.keys():
            pd.DataFrame({"ID": split[part]}).to_csv(split_path.replace(".csv", f"_{part}.csv"), index=False)
"""
            
#output_dir = "binary_survival_prediction"
#data = pd.read_csv(os.path.join(output_dir, "Clinical_data_with_labels.csv"))


output_dir = "binary_subtype_prediction_ACvsSqCC"
data = pd.read_csv(os.path.join(output_dir, "Clinical_data_with_labels.csv"))


fold_dir_10 = os.path.join(output_dir, "10foldcrossval")
k_fold_cross_validation(data, fold_dir_10)

fold_dir_100 = os.path.join(output_dir, "100foldcrossvalrepeat")
repeated_k_fold_cross_validation(data, fold_dir_100)

#fold_dir_lou = os.path.join(output_dir, "leave_one_out")
#leave_one_out_cross_validation(data, fold_dir_lou)




