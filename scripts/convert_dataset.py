import os
import numpy as np
import pandas as pd
import pretty_midi
from tqdm import tqdm

SEED = 42

def midi_to_text(midifile):
    #load midi file
    midi_data = pretty_midi.PrettyMIDI(midifile)
    #create list of notes for each instrument in midi file
    total_note_list = []
    #for now just use first instrument
    for note in midi_data.instruments[0].notes[:]:
        #change note's pitch from numerical to text value
        pitch = pretty_midi.note_number_to_name(note.pitch)
        total_note_list.append(pitch)
    return ' '.join(total_note_list)

def train_validate_test_split(df, train_percent=.7, validate_percent=.15, seed=SEED):
    np.random.seed(seed)
    perm = np.random.permutation(df.index)
    m = len(df.index)
    train_end = int(train_percent * m)
    validate_end = int(validate_percent * m) + train_end
    train = df.iloc[perm[:train_end]]
    validate = df.iloc[perm[train_end:validate_end]]
    test = df.iloc[perm[validate_end:]]
    return train, validate, test


if __name__ == "__main__":
    df = pd.DataFrame(columns=['name', 'text'])
    data = []
    for (dirpath, dirnames, filenames) in os.walk('../data/raw_midi/'):
        for filename in tqdm(filenames):
            midi_file = os.path.join(dirpath, filename)
            try:
                text = midi_to_text(midi_file)
            except:
                continue
            data.append([filename[:-4], text])
    df = pd.DataFrame(data, columns=['name', 'text'])
    df.to_csv('../data/full.csv', index=False)
    train, valid, test = train_validate_test_split(df)
    train.to_csv('../data/train.csv', index=False)
    valid.to_csv('../data/valid.csv', index=False)
    test.to_csv('../data/test.csv', index=False)