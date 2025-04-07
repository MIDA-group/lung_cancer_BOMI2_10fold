import pandas as pd

import os
from sklearn.model_selection import StratifiedKFold, train_test_split, RepeatedStratifiedKFold

def train_val_test_split(df, output_dir, labelname="label", test_size=30, val_size=0.1, random_state=42):
    """
    Splits the dataset into train, validation, and test sets.
    The test set contains exactly 15 samples from label=1 and 15 from label=0.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Separate the dataset by label
    df_label_1 = df[df[labelname] == 1]
    df_label_0 = df[df[labelname] == 0]
    
    # Ensure there are enough samples
    assert len(df_label_1) >= 15 and len(df_label_0) >= 15, "Not enough samples for test split"
    
    # Sample 15 instances from each class for the test set
    test_label_1 = df_label_1.sample(n=15, random_state=random_state)
    test_label_0 = df_label_0.sample(n=15, random_state=random_state)
    test_set = pd.concat([test_label_1, test_label_0])
    
    # Remove test samples from the dataset
    df_remaining = df.drop(test_set.index)
    
    # Split remaining data into train and validation sets
    train_set, val_set = train_test_split(df_remaining, test_size=val_size, stratify=df_remaining[labelname], random_state=random_state)
    
    # Save the splits
    splits = {"train": train_set, "val": val_set, "test": test_set, "train_val": df_remaining}
    for part, data in splits.items():
        split_path = os.path.join(output_dir, f"{part}.csv")
        data.to_csv(split_path, index=False)
    
    print("Data splits saved successfully.")
    return train_set, val_set, test_set



output_dir = "binary_subtype_prediction_ACvsSqCC"
data = pd.read_csv(os.path.join(output_dir, "Clinical_data_with_labels.csv"))


datasplit_dir = os.path.join(output_dir, "static_split")
train_val_test_split(data, datasplit_dir)


