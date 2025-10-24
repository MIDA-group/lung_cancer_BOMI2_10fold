## Partition data for survival predictions

10 non-overlapping parts of the BOMI2 data, given by the 10 test sets of the [lung_cancer_BOMI2_dataset](https://github.com/MIDA-group/lung_cancer_BOMI2_dataset/tree/main/binary_survival_prediction/10foldcrossval).

To generate 1+n+(9-n) 10-fold cross validations data, for split *i*:

test set
: part_i.csv

validation set
: part_{(i+1:n)%10}.csv - where % is the modulo operator

training set
: all other parts

