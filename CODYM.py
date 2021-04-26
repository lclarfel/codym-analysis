# Author: Dr. Laurence A. Clarfeld
# Copyright: 4/22/2021
#
# All Rights Reserved. Permission to use, copy, modify, and distribute this software
# for educational, research, and not-for-profit purposes,
# without fee and without a signed licensing agreement, is hereby granted,
# provided that the Author (Dr. Laurence A. Clarfeld) is properly credited
# and the source website is properly cited

class CODYM():

    def __init__(self, turn_lengths, model_order, *mask):
        """Populate a CODYM based on an observed sequence of binarized turn lengths
        
        Inputs:
            turn_lengths - the list of binarized turn lengths
            model_order - the order of the CODYM model
            mask - a logical mask of turns to be included in the CODYM
        Example call:
            CODYM(list(np.random.randint(0,2,100)), 2)
        """

        self.model_order = model_order
        self.turn_lengths = turn_lengths        
        self.states_order = [[int(i) for i in "{0:b}".format(j).zfill(model_order)] for j in range(2**model_order)]
        self.trans_order = [t + t[1:] + [0] for t in self.states_order] + [t + t[1:] + [1] for t in self.states_order]
        
        # FIX - trying to make this match my results
        # states = [turn_lengths[i:i+model_order] for i in range(len(turn_lengths)-model_order+1)]
        states = [turn_lengths[i:i+model_order] for i in range(len(turn_lengths)-model_order)]    
        transitions = [states[i] + states[i+1] for i in range(len(states)-1)]
    
        if len(mask):
            if not any(mask):
                print('Mask contains no selected turns, being ignored')
            else:
                states = [states[i] for i in range(len(states)) if mask[0][model_order-1:][i]]
                # FIX STARTING HERE
                transitions = [transitions[i] for i in range(len(transitions)) if mask[0][model_order:][i]]
                # transitions = [transitions[i] for i in range(len(transitions)) if mask[0][model_order-2:][i]]
    
        states_counts = [states.count(self.states_order[i]) for i in range(len(self.states_order))]
        trans_counts = [transitions.count(self.trans_order[i]) for i in range(len(self.trans_order))]
            
        self.states_obs = [i/sum(states_counts) if sum(states_counts) != 0 else 0 for i in states_counts]
        self.trans_obs = [i/sum(trans_counts) if sum(trans_counts) != 0 else 0 for i in trans_counts]
        
 
    # def populate_CODYM(turn_lengths, model_order, *mask):
    #     """Populate a CODYM based on an observed sequence of binarized turn lengths
        
    #     Inputs:
    #         turn_lengths - the list of binarized turn lengths
    #         model_order - the order of the CODYM model
    #     Example call:
    #         populate_CODYM(list((np.random.random(100) < 0.5).astype(int)), 2)
    #     """
        
    #     states_order = [[int(i) for i in "{0:b}".format(j).zfill(model_order)] for j in range(2**model_order)]
    #     trans_order = [t + t[1:] + [0] for t in CODYM['states_order']] + [t + t[1:] + [1] for t in CODYM['states_order']]
        
    #     # FIX - trying to make this match my results
    #     # states = [turn_lengths[i:i+model_order] for i in range(len(turn_lengths)-model_order+1)]
    #     states = [turn_lengths[i:i+model_order] for i in range(len(turn_lengths)-model_order)]    
    #     transitions = [states[i] + states[i+1] for i in range(len(states)-1)]
    
    #     if len(mask):
    #         if not any(mask):
    #             print('Mask contains no selected turns, being ignored')
    #         else:
    #             states = [states[i] for i in range(len(states)) if mask[0][model_order-1:][i]]
    #             # FIX STARTING HERE
    #             transitions = [transitions[i] for i in range(len(transitions)) if mask[0][model_order:][i]]
    #             # transitions = [transitions[i] for i in range(len(transitions)) if mask[0][model_order-2:][i]]
    
    #     states_counts = [states.count(CODYM['states_order'][i]) for i in range(len(CODYM['states_order']))]
    #     trans_counts = [transitions.count(CODYM['trans_order'][i]) for i in range(len(CODYM['trans_order']))]
            
    #     states_obs = [i/sum(states_counts) if sum(states_counts) != 0 else 0 for i in states_counts]
    #     trans_obs = [i/sum(trans_counts) if sum(trans_counts) != 0 else 0 for i in trans_counts]
        
    #     return CODYM(states_obs, trans_obs, states_order, trans_order)
    
    def __sub__(self, codym):
        c_new = CODYM([],self.model_order)
        c_new.states_obs = [i-j for (i,j) in zip(self.states_obs, codym.states_obs)]
        c_new.trans_obs = [i-j for (i,j) in zip(self.trans_obs, codym.trans_obs)]
        return(c_new)
        
def codym_avg(clist):
    # NOTE: This avg is NOT weighted by the number of turns in a conversation
    c_new = CODYM([], clist[0].model_order)
    c_new.states_obs = [sum(col) / len(col) for col in zip(*[c.states_obs for c in clist])]
    c_new.trans_obs = [sum(col) / len(col) for col in zip(*[c.trans_obs for c in clist])]
    return(c_new)
    
    # c_new.state_obs = list(np.mean([c.states_obs for c in clist],axis=0))
    # c_new.state_obs = list(np.mean([c.states_obs for c in clist],axis=0))
