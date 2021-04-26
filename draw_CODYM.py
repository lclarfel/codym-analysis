# Author: Dr. Laurence A. Clarfeld
# Copyright: 4/22/2021
#
# All Rights Reserved. Permission to use, copy, modify, and distribute this software
# for educational, research, and not-for-profit purposes,
# without fee and without a signed licensing agreement, is hereby granted,
# provided that the Author (Dr. Laurence A. Clarfeld) is properly credited
# and the source website is properly cited

import numpy as np
from matplotlib import pyplot as plt
from draw_order_2 import draw_order_2
from draw_order_3 import draw_order_3

def draw_codym(codym, is_diff = False):
    """Plot the state space diagram of 2nd- and 3rd-order codyms
    """
    
    opts = {} # Plotting options
    
    states_obs = codym.states_obs
    trans_obs = codym.trans_obs
    
    if is_diff:
        colormap = 'coolwarm'
        node_lim = np.ceil(np.max(np.abs(states_obs)*100))
        edge_lim = np.ceil(np.max(np.abs(trans_obs)*100))
        opts['w_range_nodes'] = (node_lim*0.8, node_lim*1.2)
        opts['w_range_edges'] = (-edge_lim, edge_lim)
    else:
        colormap = 'cool'
        opts['w_range_nodes'] = (np.floor(np.min(states_obs)*100*0.8), 
                                 np.ceil(np.max(states_obs)*100*1.2))
        opts['w_range_edges'] = (np.floor(np.min(trans_obs)*100), 
                                 np.ceil(np.max(trans_obs)*100))


              
    states_order = codym.states_order
    trans_order = codym.trans_order
    
    opts['show_edge_labels'] = True
    opts['show_node_labels'] = False
    opts['colormap'] = colormap
    opts['scale_nodes'] = False
    opts['scale_edges'] = True
    opts['diag_edge_ang_dis'] = -23

    opts['is_sig_state'] = [True]*len(codym.states_obs)
    opts['is_sig_trans'] = [True]*len(codym.trans_obs)
    
    if codym.model_order == 2:
        fig, axes = plt.subplots(1,1,figsize=(8,4))
        ax = plt.subplot(1,1,1)
        ax_return = draw_order_2(states_obs, np.array(states_order), trans_obs, np.array(trans_order), ax, opts)
    elif codym.model_order == 3:
        fig, axes = plt.subplots(1,1,figsize=(11,4))
        ax = plt.subplot(1,1,1)
        ax_return = draw_order_3(states_obs, np.array(states_order), trans_obs, np.array(trans_order), ax, opts)
    
    fig.subplots_adjust(bottom=0.08) # makes colorbar tighter with figure 
    p0 = axes.get_position().get_points().flatten()
    ax_cbar = fig.add_axes([p0[0], 0, p0[2]-p0[0], 0.05])
    cbar = plt.colorbar(ax_return, cax=ax_cbar, orientation='horizontal')
    cbar.ax.tick_params(labelsize=14)
    cbar.ax.set_xlabel('Frequency (%)',fontsize=18)
