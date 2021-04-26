# Author: Dr. Laurence A. Clarfeld
# Copyright: 4/22/2021
#
# All Rights Reserved. Permission to use, copy, modify, and distribute this software
# for educational, research, and not-for-profit purposes,
# without fee and without a signed licensing agreement, is hereby granted,
# provided that the Author (Dr. Laurence A. Clarfeld) is properly credited
# and the source website is properly cited

import numpy as np
import re

from CODYM import CODYM
from CODYM import codym_avg
from draw_CODYM import draw_codym

from convokit import Corpus, download

# Load the supreme court corpus from ConvoKit
if 'corpus' not in locals():
    corpus = Corpus(filename=download("supreme-corpus"))
    
conv_ids = [] # ID of each conversation
convs = [] # Number of words in each speaker utterance, for each conversation
speakers = [] # Speaker of each utterance, for each conversation

for conv in corpus.iter_conversations():

    turn = [] # All words in the utterance
    speaker = [] # Speaker of each turn, for each conversation
    n_words = [] # Number of words per turn, for each conversation

    for utt in conv.iter_utterances():
        turn = utt.text
        
        # Replace dashes (-), periods (.), apostrophes (') and slashes (/) with spaces
        turn = re.sub("[-./']",' ',turn) 
        
        # Remove other punctuation (,?!";:)
        turn = re.sub('[,?!";:]','',turn) # remove punctuation
        
        # Replace double spaces w/ single ones
        turn = re.sub('[ ]{2,}',' ',turn) 
        
        n_words.append(turn.count(' ')+1)
        
        # Alternatively, use gender to define a speaker:
        # speaker.append(1 if utt.speaker.meta['sex'] == 'FEMALE' else 0)
        
        # Speaker 1 indicates a supreme court justice, 0 indicates not a justice
        if utt.speaker.meta['is-justice']:
            speaker.append(1)
        else:
            speaker.append(0)
            
    # Only include cases with 20 or more turns.
    if len(n_words) >= 20:
        conv_ids.append(conv.get_id())
        convs.append(n_words)
        speakers.append(speaker)

# Binarize turn lengths
t = np.round(np.median(np.hstack(convs))) # The short/long threshold
turn_lens_all_convs = [[int(l >= t) for l in conv] for conv in convs]

# Define a CODYM model for each conversation
CODYMS = []
for i in range(len(convs)):
    turn_lengths = turn_lens_all_convs[i]
    speaker = speakers[i]
    speaker = [1 if not i else 0 for i in speaker]
    CODYMS.append(CODYM(turn_lengths,3,speaker))

codym_norm = codym_avg(CODYMS)

draw_codym(codym_norm) # Draw the normative CODYM
