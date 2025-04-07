import pandas as pd
import os
from ydata_profiling import ProfileReport

data_dir = "binary_survival_prediction"
data = pd.read_csv(os.path.join(data_dir, "Clinical_data_with_labels.csv"))

profile = ProfileReport(data, title="Profiling Report")
profile.to_file("report.html")

