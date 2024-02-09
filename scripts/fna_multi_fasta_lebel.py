from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os
from Bio import SeqIO
import pandas as pd

def label_all_genomes(input_name, label_file, out_path):
    if out_path is None:
        out_path = os.getcwd()
    output_name = os.path.join(out_path, 'label_' + input_name)
    train_labels = pd.read_csv(label_file)
    label_dict = {train_labels['id'][i]: train_labels['y_true'][i] for i in range(len(train_labels))}
    with open(input_name) as original, open(output_name, 'w') as corrected:
        records = SeqIO.parse(input_name, 'fasta')
        for record in records:         
            old_record = record.id
            y_true = label_dict.get(old_record)
            new_record = f"{old_record}|{y_true}"
            record.id = new_record
            record.description = new_record
            SeqIO.write(record, corrected, 'fasta')
    return

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='input_fasta', type=str,
                        help='/path/to/iput.fasta')
    parser.add_argument('-m', dest='map_file', type=str,
                        help='/path/to/map_file.txt')
    parser.add_argument('-o', dest='out_path', type=str, default=None,
                        help='/path/to/output_dir')

    args = parser.parse_args()
    input_fasta = args.input_fasta
    map_file = args.map_file
    out_path = args.out_path

    label_all_genomes(input_fasta, map_file, out_path)

    return


if __name__ == '__main__':
    main()