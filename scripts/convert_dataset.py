import os
import numpy as np
import pandas as pd
import pretty_midi
from miditok import OctupleMono, REMI
from miditoolkit import MidiFile
from tqdm import tqdm
from pathlib import Path

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
    df = pd.DataFrame(columns=['name', 'tokens'])
    data = []
    # Creates the tokenizer and list the file paths
    tokenizer = REMI() 
    paths = list(Path('../data/raw_midi').glob('**/*.mid'))

    def midi_valid(midi) -> bool:
        if any(ts.numerator != 4 for ts in midi.time_signature_changes):
            return False  # time signature different from 4/*, 4 beats per bar
        if midi.max_tick < 10 * midi.ticks_per_beat:
            return False  # this MIDI is too short
        return True

    # Converts MIDI files to tokens saved as JSON files
    for path in tqdm(paths):
        try:
            midi = MidiFile(path)
            if midi_valid(midi):
                data.append([path.name[:-4], tokenizer.midi_to_tokens(midi)[0]])
        except:
            continue


    # for (dirpath, dirnames, filenames) in os.walk('../data/raw_midi/'):
    #     for filename in tqdm(filenames):
    #         midi_file = os.path.join(dirpath, filename)
    #         try:
    #             text = midi_to_text(midi_file)
    #         except:
    #             continue
    #         data.append([filename[:-4], text])

    df = pd.DataFrame(data, columns=['name', 'tokens'])
    df.to_csv('../data/full.csv', index=False)
    train, valid, test = train_validate_test_split(df)
    train.to_csv('../data/train.csv', index=False)
    valid.to_csv('../data/valid.csv', index=False)
    test.to_csv('../data/test.csv', index=False)