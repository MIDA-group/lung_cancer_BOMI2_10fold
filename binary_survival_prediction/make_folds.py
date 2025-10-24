import csv
import os

test_parts = 1
val_parts = 3
total_parts = 10
train_parts = total_parts-val_parts-test_parts

# input paths
parts_dir = '10parts'
parts_format = 'part_{}.csv'

# output paths
folds_dir = '10folds'
folds_format = 'fold_{}_{}.csv'

def offset(i,fold):
    return (i+fold)%total_parts

def make_fold(fold):
    test_set = []
    for i in (offset(j,fold) for j in range(test_parts)):
        with open(os.path.join(parts_dir, parts_format.format(i)), 'r') as f:
            reader = csv.DictReader(f)
            test_set += [row['ID'] for row in reader]

    val_set = []
    for i in (offset(j+test_parts,fold) for j in range(val_parts)):
        with open(os.path.join(parts_dir, parts_format.format(i)), 'r') as f:
            reader = csv.DictReader(f)
            val_set += [row['ID'] for row in reader]

    train_set = []
    for i in (offset(j+test_parts+val_parts,fold) for j in range(train_parts)):
        with open(os.path.join(parts_dir, parts_format.format(i)), 'r') as f:
            reader = csv.DictReader(f)
            train_set += [row['ID'] for row in reader]

    return {'test':test_set,'val':val_set,'train':train_set}

def write_fold(fold, data):
    for s in ('test','val','train'):
        with open(os.path.join(folds_dir, folds_format.format(fold,s)), 'w', newline='') as f:
            writer = csv.writer(f, lineterminator=os.linesep)
            writer.writerow(['ID'])
            writer.writerows(zip(data[s]))

for fold in range(total_parts):
    data = make_fold(fold)

    os.makedirs(folds_dir, exist_ok=True)
    write_fold(fold,data)

