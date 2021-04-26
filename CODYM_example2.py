# Author: Dr. Laurence A. Clarfeld
# Copyright: 4/22/2021
#
# All Rights Reserved. Permission to use, copy, modify, and distribute this software
# for educational, research, and not-for-profit purposes,
# without fee and without a signed licensing agreement, is hereby granted,
# provided that the Author (Dr. Laurence A. Clarfeld) is properly credited
# and the source website is properly cited

import numpy as np
import pandas as pd

from CODYM import CODYM
from CODYM import codym_avg
from draw_CODYM import draw_codym

data = pd.read_csv('S1_dataset.csv', header=1)

# For each conversation
CODYMS_with_emo = []
CODYMS_without_emo = []

for conv_num in np.unique(data['conv_num']):
    
    conv_mask = data['conv_num'] == conv_num
    emo_mask = list(np.any(data[conv_mask][['has_anger','has_fear']].values,axis=1).astype(int))
    speaker_mask = list(data[conv_mask]['speaker']==0) # patient turns only
    tur_lens = list((data[conv_mask]['n_words'] >= 8).values.astype(int))
    
    if any(emo_mask):
        CODYMS_with_emo.append(CODYM(tur_lens, 3, speaker_mask))
    else:
        CODYMS_without_emo.append(CODYM(tur_lens, 3, speaker_mask))        
        
CODYM_emo = codym_avg(CODYMS_with_emo) - codym_avg(CODYMS_without_emo)

draw_codym(CODYM_emo, True) # Draw the normative difference CODYM
