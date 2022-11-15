import pretty_midi

def midiToText(midifile):
    #load midi file
    midi_data = pretty_midi.PrettyMIDI(midifile)
    #create list of notes for each instrument in midi file
    total_note_list = []
    #loop over all instruments in midi file
    for i in range(len(midi_data.instruments[:])):
        #create list of notes for each instrument
        single_instrument_note_list = []
        for note in midi_data.instruments[i].notes[:]:
            #change note's pitch from numerical to text value
            note.pitch = pretty_midi.note_number_to_name(note.pitch)
            single_instrument_note_list.append(note)
        total_note_list.append(single_instrument_note_list)
    return total_note_list

print(midiToText('VampireKillerCV1.mid'))