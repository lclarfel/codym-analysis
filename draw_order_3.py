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
from matplotlib import patches

def draw_order_3(states_obs, states_order, trans_obs, trans_order, ax, opts):
    
    
    # Assign plotting parameters

    # GENERAL
    fig_dpi = 72
    h = 3 # Height of diagram
    w = 6 # With of diagram
    w1 = 1.2 # Displacement of first set of points
    
    
    # NODE CHARACTERISTICS
    show_node_inlabels = True # Show node label inside node
    innode_lbl_color = 'w'
    node_size = 700 # Size of nodes, when un-scaled
    node_edge_width = 2
    node_lbl_size = 12
    non_sig_node_color = 'darkgray'
    sig_node_color = 'k'
    if 'w_range_nodes' not in opts:
        opts['w_range_nodes'] = (np.floor(np.min(states_obs)*100*0.9), 
                                 np.ceil(np.max(states_obs)*100*1.1))
    
    # EDGE CHARACTERISTICS
    se_d = 0.2 # straight-edge displacement
    ar_se_d = 0.78 # Arrow proportion (to align correctly) for straight edges
    il_d = 0.12 # Extra displacement for inner loop edges
    a_c = 12 # 5 # Extra displacement prevents self-loop arc from overlapping arrowhead
    r_c = 0.75 # Radius for self-loop circles
    a_d = 28 # Displacement of inner edges (in degrees)
    d_inner = 0.17 # Vertical displacement of inner-loop arrows from center
    non_sig_style = '--' # Dashed edges for non-significant transitions
    sig_style = '-' # Solid edges for significant transitions 
    max_edge_width = 8 # If scaling edges
    min_edge_width = 2 # If scaling edges
    edge_width = 2.5 # Width of self-loop lines
    inner_arc_rad = 0.7
    inner_arc = "arc3,rad=" + str(inner_arc_rad) # "Connection Style", size of arc on inner-loop
    a_d_selfloop = 45 # Controls location of arrowhead on self-loops
    ar_vert = 0.07 # Controls location of arrowhead on self-loops
    ar_horiz = 0.04 # Controls location of arrowhead on self-loops
    
    if 'w_range_edges' not in opts:
        opts['w_range_edges'] = (np.floor(np.min(trans_obs)*100*1), 
                                 np.ceil(np.max(trans_obs)*100*1))
        
    # Edge label characteristics
    edge_label_font_size = 14
    edge_label_color = 'k'
    a_t = -2 # Adjust angles by this amount
    d_n = 0.25 # How much to displace node label
    
    
    # Node order (for plotting)
    states_all = np.array([[0., 0., 0.],
                           [0., 0., 1.],
                           [0., 1., 0.],
                           [0., 1., 1.],
                           [1., 0., 0.],
                           [1., 0., 1.],
                           [1., 1., 0.],
                           [1., 1., 1.]])
    
    # Edge order (for plotting)
    transition_all =  np.array([[0., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 1.],
                                [0., 0., 1., 0., 1., 0.],
                                [0., 0., 1., 0., 1., 1.],
                                [0., 1., 0., 1., 0., 0.],
                                [0., 1., 0., 1., 0., 1.],
                                [0., 1., 1., 1., 1., 0.],
                                [0., 1., 1., 1., 1., 1.],
                                [1., 0., 0., 0., 0., 0.],
                                [1., 0., 0., 0., 0., 1.],
                                [1., 0., 1., 0., 1., 0.],
                                [1., 0., 1., 0., 1., 1.],
                                [1., 1., 0., 1., 0., 0.],
                                [1., 1., 0., 1., 0., 1.],
                                [1., 1., 1., 1., 1., 0.],
                                [1., 1., 1., 1., 1., 1.]])
    

    #><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><
    # Fix the ordering and add for any missing states
    #><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><
    
    # Fill in any missing STATES w/ zeros and fix the ordering
    temp_states = []
    for state in states_all:
        i_state = np.where(np.all(states_order==state,axis=1))[0] # matching index from observed data
        if len(i_state):
            temp_states.append(states_obs[i_state[0]])
        else:
            temp_states.append(0)
    states_obs = temp_states
    
    # Fill in any missing TRANSITIONS w/ zeros and fix the ordering
    temp_trans = []
    temp_trans_sig = []
    for trans in transition_all:
        
        i_trans = np.where(np.all(trans_order==trans,axis=1))[0] # matching index from observed data
        if len(i_trans):
            temp_trans.append(trans_obs[i_trans[0]])
            temp_trans_sig.append(opts['is_sig_trans'][i_trans[0]])
        else:
            temp_trans.append(0)
    trans_obs = temp_trans
    opts['is_sig_trans'] = temp_trans_sig    
    
    #><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><
    # 
    #><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><
    
    # convert frequencies to percents to use as weights
    node_weights = np.array(states_obs)*100
    edge_weights = np.array(trans_obs)*100
            
    
    #>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-
    #>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-
    
    # Edge labels
    if opts['scale_edges']:
        t_d = 0.26
    else:
        t_d = 0.18 # text displacement for edge labels
    
    # Edges that are NOT curvy (i.e., excluding SSS->S, LLL->L, LSL->S, and SLS->L)
    E_straight = np.array([[0,1],[1,2],[2,4],[4,0],[1,3],[6,4],[5,3],[3,7],[7,6],[6,5],[3,6],[4,1]]) 
    E_straight_i = [1,2,4,8,3,12,11,7,14,13,6,9] # Matching indexes to get from E_straight to E (for adding weights)
    node_lbls = ['SSS','SSL','SLS','SLL','LSS','LSL','LLS','LLL']
    
    # Node positions
    node_pos = [[] for _ in range(8)]
    node_pos[0] = (0,h/2)
    node_pos[1] = (w1,h)
    node_pos[2] = (w1+w1,h/2)
    node_pos[3] = (w-w1,h)
    node_pos[4] = (w1,0)
    node_pos[5] = (w-(w1+w1),h/2)
    node_pos[6] = (w-w1,0)
    node_pos[7] = (w,h/2)
        
    # Plot the nodes
    node_pos_arr = np.array(node_pos) # Get into good numpy format
    cm = plt.cm.get_cmap(opts['colormap']) # Assign colormap
    
    # Set node sizing
    if opts['scale_nodes']:
        node_min_size = 500
        node_max_size = 2600
        
        node_sizes = (np.abs(node_weights)+1)**1.8*9.2 # Heuristic has worked well for node sizing
        # This is as big/small as a node can get, based on the weight
        min_weight_adj = (np.abs(opts['w_range_nodes'][0])+1)**1.8*9.2
        max_weight_adj = (np.abs(opts['w_range_nodes'][1])+1)**1.8*9.2
        
        if min_weight_adj == max_weight_adj:
            node_sizes = np.ones(8)*1000
        else:
            node_sizes = (node_sizes-min_weight_adj)/(max_weight_adj-min_weight_adj) # This normalizes into a scale of [0,1] based on w_range
            node_sizes = node_sizes*(node_max_size-node_min_size) + node_min_size
            # node_sizes = ((node_sizes-np.min(node_sizes))*(node_max_size-node_min_size))/(np.max(node_sizes)-np.min(node_sizes))+node_min_size
    else:
        node_sizes = node_size*np.ones(8)
        
    sl_d_000 = np.sqrt(node_sizes[0])**0.8/50 # Additional offset for SSS-loop, by node size
    sl_d_111 = np.sqrt(node_sizes[7])**0.8/50 # Additional offset for LLL-loop, by node size
    
    n_color = []
    for ii in range(8):
        if opts['is_sig_state'][ii]:
            n_color.append(sig_node_color)
        else:
            n_color.append(non_sig_node_color)
    plt.scatter(node_pos_arr[:,0],node_pos_arr[:,1],s=node_sizes,c=n_color,edgecolors=n_color,linewidth=node_edge_width,cmap=cm,linestyle='-',zorder=3)
    
    if opts['scale_edges']:
        sc = plt.scatter(np.zeros(16),np.zeros(16),s=np.zeros(8),c=edge_weights,cmap=cm)
    
    plt.clim(opts['w_range_edges'][0], opts['w_range_edges'][1]) # Set max/min limits for the colorbar
    
    for i in range(8):
        if show_node_inlabels:
            plt.annotate(node_lbls[i],[node_pos[i][0],node_pos[i][1]],ha='center',va='center',color=innode_lbl_color,weight='bold',fontsize=node_lbl_size)
    
    # Plot all of the straight-line edges (including offsets for node size)
    for i in range(len(E_straight)):
    
        nodes = E_straight[i] # Get TO and FROM nodes for the straight edge
        
        inv = ax.transData.inverted()
        rpix_r_from = node_sizes[nodes[0]]**0.5/2*fig_dpi/72
        act_r_from = inv.transform([rpix_r_from,rpix_r_from])-inv.transform([0,0])
    
        # inv = ax.transData.inverted()
        rpix_r_to = node_sizes[nodes[1]]**0.5/2*fig_dpi/72
        act_r_to = inv.transform([rpix_r_to,rpix_r_to])-inv.transform([0,0])

                
        if opts['scale_edges']:
            w_range = opts['w_range_edges'] # Weight range for colormap
            color_i = (edge_weights[E_straight_i[i]]-w_range[0])/(w_range[1]-w_range[0])
            edge_color = cm(color_i)
            ew = (np.abs(edge_weights[E_straight_i[i]])-0)/(w_range[1]-0)*(max_edge_width-min_edge_width)+min_edge_width
        else:
            ew = edge_width
            edge_color = 'k'
        
        # Style lines based on whether specified as significant
        if opts['is_sig_trans'][E_straight_i[i]]:
            ls = sig_style
        else:
            ls = non_sig_style
        
        # Extra dispalcement based on line width
        rpix_r_e = ew/2*fig_dpi/72
        act_r_e = inv.transform([rpix_r_e,rpix_r_e])-inv.transform([0,0])
        
        style_s ="Simple,tail_width=1.5,head_width=" + str(ew*1.3) + ",head_length=" + str(ew*1.3*1.25)
        
        # Case for straight, HORIZONTAL edges (SSL->L and LLS->S)
        if (i == 4) or (i == 5):
            if i == 4:                
                plt.plot([node_pos[nodes[0]][0]+act_r_from[0]+act_r_e[0]+se_d,
                          node_pos[nodes[1]][0]-act_r_to[0]-act_r_e[0]-se_d],
                          [node_pos[nodes[0]][1],
                           node_pos[nodes[1]][1]],
                          linestyle=ls,color = edge_color,linewidth=ew,zorder=4)
                
                a = patches.FancyArrowPatch([node_pos[nodes[1]][0]-act_r_to[0]-act_r_e[0]-se_d*0.8-0.05,
                                             node_pos[nodes[1]][1]],
                                            [node_pos[nodes[1]][0]-act_r_to[0]-act_r_e[0]-se_d*0.8,
                                             node_pos[nodes[1]][1]],
                                            color=edge_color,linewidth=ew,arrowstyle=style_s) 
                
            elif i == 5:                
                plt.plot([node_pos[nodes[0]][0]-act_r_from[0]-act_r_e[0]-se_d,
                          node_pos[nodes[1]][0]+act_r_to[0]+act_r_e[0]+se_d],
                          [node_pos[nodes[0]][1],
                           node_pos[nodes[1]][1]],
                          linestyle=ls,color = edge_color,linewidth=ew,zorder=3)
    
                a = patches.FancyArrowPatch([node_pos[nodes[1]][0]+act_r_to[0]+act_r_e[0]+se_d*0.8+0.05,
                                             node_pos[nodes[1]][1]],
                                            [node_pos[nodes[1]][0]+act_r_to[0]+act_r_e[0]+se_d*0.8,
                                             node_pos[nodes[1]][1]],
                                            color=edge_color,linewidth=ew,arrowstyle=style_s) 
            
        # Case for straight, VERTICAL edges (SLL->S and LSS->L)
        elif (i == 10) or (i == 11):    
            
            if i == 10:
                
                plt.plot([node_pos[nodes[0]][0],
                          node_pos[nodes[1]][0]],
                          [node_pos[nodes[0]][1]-act_r_from[1]-act_r_e[1]-se_d,
                            node_pos[nodes[1]][1]+act_r_to[1]+act_r_e[1]+se_d],
                          linestyle=ls,color = edge_color,linewidth=ew,zorder=3)
                
                a = patches.FancyArrowPatch([node_pos[nodes[1]][0],
                                             node_pos[nodes[1]][1]+act_r_to[1]+act_r_e[1]+se_d*0.8+0.05],
                                            [node_pos[nodes[1]][0],
                                             node_pos[nodes[1]][1]+act_r_to[1]+act_r_e[1]+se_d*0.8],
                                            color=edge_color,linewidth=ew,arrowstyle=style_s) 
                
            elif i == 11:
                plt.plot([node_pos[nodes[0]][0],
                          node_pos[nodes[1]][0]],
                          [node_pos[nodes[0]][1]+act_r_from[1]+act_r_e[1]+se_d,
                            node_pos[nodes[1]][1]-act_r_to[1]-act_r_e[1]-se_d],
                          linestyle=ls,color = edge_color,linewidth=ew,zorder=3)
                
                a = patches.FancyArrowPatch([node_pos[nodes[1]][0],
                                             node_pos[nodes[1]][1]-act_r_to[1]-act_r_e[1]-se_d*0.8-0.05],
                                            [node_pos[nodes[1]][0],
                                             node_pos[nodes[1]][1]-act_r_to[1]-act_r_e[1]-se_d*0.8],
                                            color=edge_color,linewidth=ew,arrowstyle=style_s) 
            
        # Cases for all the diagonal edges
        else:
            if (i == 0) or (i == 6):
                plt.plot([node_pos[nodes[0]][0]+(act_r_from[0]+act_r_e[0]+se_d)/np.sqrt(2),
                          node_pos[nodes[1]][0]-(act_r_to[0]+act_r_e[0]+se_d)/np.sqrt(2)],
                          [node_pos[nodes[0]][1]+(act_r_from[1]+act_r_e[1]+se_d)/np.sqrt(2),
                            node_pos[nodes[1]][1]-(act_r_to[1]+act_r_e[1]+se_d)/np.sqrt(2)],
                          linestyle=ls,color = edge_color,linewidth=ew,zorder=3) 

                a = patches.FancyArrowPatch([node_pos[nodes[1]][0]-(act_r_to[0]+act_r_e[0]+se_d)/np.sqrt(2)*ar_se_d-0.05,
                                             node_pos[nodes[1]][1]-(act_r_to[1]+act_r_e[1]+se_d)/np.sqrt(2)*ar_se_d-0.05*(1.3)],
                                            [node_pos[nodes[1]][0]-(act_r_to[0]+act_r_e[0]+se_d)/np.sqrt(2)*ar_se_d,
                                             node_pos[nodes[1]][1]-(act_r_to[1]+act_r_e[1]+se_d)/np.sqrt(2)*ar_se_d],
                                            color=edge_color,linewidth=ew,arrowstyle=style_s)
                
            elif (i == 1) or (i == 7):            
                plt.plot([node_pos[nodes[0]][0]+(act_r_from[0]+act_r_e[0]+se_d)/np.sqrt(2),
                          node_pos[nodes[1]][0]-(act_r_to[0]+act_r_e[0]+se_d)/np.sqrt(2)],
                          [node_pos[nodes[0]][1]-(act_r_from[1]+act_r_e[1]+se_d)/np.sqrt(2),
                            node_pos[nodes[1]][1]+(act_r_to[1]+act_r_e[1]+se_d)/np.sqrt(2)],
                          linestyle=ls,color = edge_color,linewidth=ew,zorder=3) 
                a = patches.FancyArrowPatch([node_pos[nodes[1]][0]-(act_r_to[0]+act_r_e[0]+se_d)/np.sqrt(2)*0.8-0.05*(act_r_to[0]/act_r_to[1]),
                                             node_pos[nodes[1]][1]+(act_r_to[1]+act_r_e[1]+se_d)/np.sqrt(2)*0.8+0.05],
                                            [node_pos[nodes[1]][0]-(act_r_to[0]+act_r_e[0]+se_d)/np.sqrt(2)*0.8,
                                             node_pos[nodes[1]][1]+(act_r_to[1]+act_r_e[1]+se_d)/np.sqrt(2)*0.8],
                                            color=edge_color,linewidth=ew,arrowstyle=style_s)
                
            elif (i == 2) or (i == 8):
                plt.plot([node_pos[nodes[0]][0]-(act_r_from[0]+act_r_e[0]+se_d)/np.sqrt(2),
                          node_pos[nodes[1]][0]+(act_r_to[0]+act_r_e[0]+se_d)/np.sqrt(2)],
                          [node_pos[nodes[0]][1]-(act_r_from[1]+act_r_e[1]+se_d)/np.sqrt(2),
                            node_pos[nodes[1]][1]+(act_r_to[1]+act_r_e[1]+se_d)/np.sqrt(2)],
                          linestyle=ls,color = edge_color,linewidth=ew,zorder=3)         
                a = patches.FancyArrowPatch([node_pos[nodes[1]][0]+(act_r_to[0]+act_r_e[0]+se_d)/np.sqrt(2)*0.8+0.05*(act_r_to[0]/act_r_to[1]),
                                             node_pos[nodes[1]][1]+(act_r_to[1]+act_r_e[1]+se_d)/np.sqrt(2)*0.8+0.05],
                                            [node_pos[nodes[1]][0]+(act_r_to[0]+act_r_e[0]+se_d)/np.sqrt(2)*0.8,
                                             node_pos[nodes[1]][1]+(act_r_to[1]+act_r_e[1]+se_d)/np.sqrt(2)*0.8],
                                            color=edge_color,linewidth=ew,arrowstyle=style_s)
    
            elif (i == 3) or (i == 9):  
                plt.plot([node_pos[nodes[0]][0]-(act_r_from[0]+act_r_e[0]+se_d)/np.sqrt(2),
                          node_pos[nodes[1]][0]+(act_r_to[0]+act_r_e[0]+se_d)/np.sqrt(2)],
                          [node_pos[nodes[0]][1]+(act_r_from[1]+act_r_e[1]+se_d)/np.sqrt(2),
                            node_pos[nodes[1]][1]-(act_r_to[1]+act_r_e[1]+se_d)/np.sqrt(2)],
                          linestyle=ls,color = edge_color,linewidth=ew,zorder=3)     
                a = patches.FancyArrowPatch([node_pos[nodes[1]][0]+(act_r_to[0]+act_r_e[0]+se_d)/np.sqrt(2)*0.8+0.05*(act_r_to[0]/act_r_to[1]),
                                             node_pos[nodes[1]][1]-(act_r_to[1]+act_r_e[1]+se_d)/np.sqrt(2)*0.8-0.05],
                                            [node_pos[nodes[1]][0]+(act_r_to[0]+act_r_e[0]+se_d)/np.sqrt(2)*0.8,
                                             node_pos[nodes[1]][1]-(act_r_to[1]+act_r_e[1]+se_d)/np.sqrt(2)*0.8],
                                            color=edge_color,linewidth=ew,arrowstyle=style_s)

            
        ax.add_patch(a) # Add the arrow to the plot
    
    # Self-loop edges (without arrowheads)
        
    if opts['is_sig_trans'][0]:
        ls = sig_style
    else:
        ls = non_sig_style
        
    if opts['scale_edges']:
        color_i = (edge_weights[0]-w_range[0])/(w_range[1]-w_range[0])
        edge_color_000_0 = cm(color_i)
        ew_000_0 = (np.abs(edge_weights[0])-0)/(w_range[1]-0)*(max_edge_width-min_edge_width)+min_edge_width
        
        color_i = (edge_weights[5]-w_range[0])/(w_range[1]-w_range[0])
        edge_color_010_1 = cm(color_i)
        ew_010_1 = (np.abs(edge_weights[5])-0)/(w_range[1]-0)*(max_edge_width-min_edge_width)+min_edge_width     
        
        color_i = (edge_weights[10]-w_range[0])/(w_range[1]-w_range[0])
        edge_color_101_0 = cm(color_i)       
        ew_101_0 = (np.abs(edge_weights[10])-0)/(w_range[1]-0)*(max_edge_width-min_edge_width)+min_edge_width     
        
        color_i = (edge_weights[15]-w_range[0])/(w_range[1]-w_range[0])
        edge_color_111_1 = cm(color_i)
        ew_111_1 = (np.abs(edge_weights[15])-0)/(w_range[1]-0)*(max_edge_width-min_edge_width)+min_edge_width
    else:
        ew_000_0 = edge_width
        ew_010_1 = edge_width
        ew_101_0 = edge_width
        ew_111_1 = edge_width
        
        edge_color_000_0 = 'k'
        edge_color_010_1 = 'k'
        edge_color_101_0 = 'k'
        edge_color_111_1 = 'k'
        
    p1 = patches.Arc([-r_c/2-sl_d_000,h/2], r_c, r_c, angle=0.0, theta1 = a_d + a_c, theta2 = 360 - a_d,linewidth=ew_000_0,linestyle=ls,color=edge_color_000_0)
    
    if opts['is_sig_trans'][15]:
        ls = sig_style
    else:
        ls = non_sig_style
    
    p2 = patches.Arc([w+r_c/2+sl_d_111,h/2], r_c, r_c, angle=0.0, theta1 = 180+a_d + a_c, theta2 = 180 - a_d,linewidth=ew_111_1,linestyle=ls,color=edge_color_111_1)
    
    dx = w - 2*(w1 + w1)
    dx /= np.sqrt(dx**2)

    inv = ax.transData.inverted()
    
    rpix_r_010 = node_sizes[2]**0.5/2*fig_dpi/72
    rpix_r_101 = node_sizes[5]**0.5/2*fig_dpi/72
    
    
    act_r_010 = inv.transform([rpix_r_010,rpix_r_010])-inv.transform([0,0])
    act_r_101 = inv.transform([rpix_r_101,rpix_r_101])-inv.transform([0,0])
    
    style_010_1="Simple,tail_width=1.5,head_width=" + str(min([ew_010_1,7])*1.3) + ",head_length=" + str(min([ew_010_1,7])*1.3*1.25)
    p3= patches.FancyArrowPatch([w-(w1+w1)-act_r_101[0]-il_d-ar_horiz,
                                  h/2-il_d-ar_vert],
                                [w-(w1+w1)-act_r_101[0]-il_d,
                                  h/2-il_d],
                                arrowstyle=style_010_1,color=edge_color_010_1,linewidth=ew_010_1)
    
    style_101_0="Simple,tail_width=1.5,head_width=" + str(min([ew_101_0,7])*1.3) + ",head_length=" + str(min([ew_101_0,7])*1.3*1.25)
    p4= patches.FancyArrowPatch([w1+w1+act_r_010[0]+il_d+ar_horiz,
                                 h/2+il_d+ar_vert],
                                [w1+w1+act_r_010[0]+il_d,
                                 h/2+il_d],
                                arrowstyle=style_101_0,color=edge_color_101_0,linewidth=ew_101_0)
    
    ax.add_patch(p1) # SSS shaft
    ax.add_patch(p2) # LLL shaft
    ax.add_patch(p3) # SLS -> LSL arrowhead
    ax.add_patch(p4) # LSL -> SLS arrowhead
    
    # Arrow shaft for p3
    if opts['is_sig_trans'][5]:
        ls = sig_style
    else:
        ls = non_sig_style    
    
    y1 = [w1+w1+act_r_010[0]+il_d, h/2-d_inner]
    x1 = [w-(w1+w1)-act_r_101[0]-il_d,h/2-d_inner]
    
    
    ax.annotate("",
                xy=(x1[0], x1[1]), xycoords='data',
                xytext=(y1[0], y1[1]), textcoords='data',
                arrowprops=dict(arrowstyle="-", color=edge_color_010_1,
                                shrinkA=5, shrinkB=5,
                                patchA=None, patchB=None,
                                connectionstyle=inner_arc,
                                linestyle=ls,
                                linewidth=ew_010_1)
                )
    
    
    inv = ax.transData.inverted()
    
    # Arrow shaft for p4
    
    if opts['is_sig_trans'][10]:
        ls = sig_style
    else:
        ls = non_sig_style    
    
    y1 = [w-(w1+w1)-act_r_101[0]-il_d, h/2+d_inner]
    x1 = [w1+w1+act_r_010[0]+il_d,h/2+d_inner]
    
    ax.annotate("",
                xy=(x1[0], x1[1]), xycoords='data',
                xytext=(y1[0], y1[1]), textcoords='data',
                arrowprops=dict(arrowstyle="-", color=edge_color_101_0,
                                shrinkA=5, shrinkB=5,
                                patchA=None, patchB=None,
                                connectionstyle=inner_arc,
                                linestyle=ls,
                                linewidth=ew_101_0,)
                )
        
    theta = np.deg2rad(a_d_selfloop)
    yy = r_c * np.sin(theta)
    xx = r_c - r_c * np.cos(theta)
    d_yy = r_c * np.sin(theta-.001)
    d_xx = r_c - r_c * np.cos(theta-.001)
    style_000_0 ="Simple,tail_width=1.5,head_width=" + str(ew_000_0*1.3) + ",head_length=" + str(ew_000_0*1.3*1.25)
    
    p5= patches.FancyArrowPatch([-xx/2-sl_d_000+ar_horiz,h/2+yy/2-ar_vert],[-d_xx/2-sl_d_000+ar_horiz,h/2+d_yy/2-ar_vert],arrowstyle=style_000_0,color=edge_color_000_0,linewidth=ew_000_0*1.2)
    
    yy = -r_c * np.sin(theta)
    xx = r_c - r_c * np.cos(theta)
    d_yy = -r_c * np.sin(theta-.001)
    d_xx = r_c - r_c * np.cos(theta-.001)
    style_111_1 ="Simple,tail_width=1.5,head_width=" + str(ew_111_1*1.3) + ",head_length=" + str(ew_111_1*1.3*1.25)
    
    p6= patches.FancyArrowPatch([w+xx/2+sl_d_111-ar_horiz,h/2+yy/2+ar_vert],[w+d_xx/2+sl_d_111-ar_horiz,h/2+d_yy/2+ar_vert],arrowstyle=style_111_1,color=edge_color_111_1,linewidth=ew_111_1)
    ax.add_patch(p5) # SSS arrowhead
    ax.add_patch(p6) # LLL arrowhead
    
    # Node order (for plotting)
    states_all = np.array([[0., 0., 0.],
                           [0., 0., 1.],
                           [0., 1., 0.],
                           [0., 1., 1.],
                           [1., 0., 0.],
                           [1., 0., 1.],
                           [1., 1., 0.],
                           [1., 1., 1.]])
                
    node_label_loc = [[0-d_n,h/2],
                      [w1-d_n,h],
                      [w1+w1-d_n,h/2],
                      [w-w1+d_n,h],
                      [w1-d_n,0],
                      [w-(w1+w1)+d_n,h/2],
                      [w-w1+d_n,0],
                      [w+d_n,h/2]]
    
    
    #########################################################################
    #########################################################################
    # Node Labels
    
    # Vertical/horizontal alignments of node labels
    node_label_va = ['center' for _ in range(8)] 
    node_label_ha = ['right','right','right','left','right','left','left','left']
    
    if opts['show_node_labels']:
        # Convert weights to strings for labelling
        node_labels = [str(round(nw,1)) for nw in node_weights] # NOTE, 1 sig fig
        
        for i in range(8):
            # Calculate offsets based on node size
            if i in [0, 1, 2, 4]:
                # Left-shifted
                node_lbl_offset = -np.sqrt(node_sizes[i])**0.8/130
            else:
                # Right-shifted
                node_lbl_offset = np.sqrt(node_sizes[i])**0.8/130 
            plt.annotate(node_labels[i],
                         [node_label_loc[i][0]+node_lbl_offset,node_label_loc[i][1]],
                         ha=node_label_ha[i],
                         va=node_label_va[i],
                         fontsize = node_lbl_size,
                         fontweight='bold')
    
    
    #########################################################################
    #########################################################################
    # Edge Labels
    edge_default_labels = ['L' if i%2 else 'S' for i in range(16)]
    
    edge_label_locs = [
            [-r_c/2,h/2+r_c/2+t_d], # ['SSS->SSS',
            [w1/2-t_d,3*h/4+t_d], #  'SSS->SSL',
            [w1+w1/2+t_d,3*h/4+t_d], #  'SSL->SLS',
            [w/2,h+t_d], #  'SSL->SLL',
            [w1+w1/2+t_d,h/4-t_d], #  'SLS->LSS',
            [w/2 + (act_r_010[0]-act_r_101[0])/2,h/2-r_c/2-t_d], #  'SLS->LSL',
            [w-w1+t_d/2,h/2], #  'SLL->LLS',
            [w-w1/2+t_d,3*h/4+t_d], #  'SLL->LLL',
            [w1/2-t_d,h/4-t_d], #  'LSS->SSS',
            [w1-t_d*0.5,h/2], #  'LSS->SSL',
            [w/2 + (act_r_010[0]-act_r_101[0])/2,h/2+r_c/2+t_d], #  'LSL->SLS',
            [w-(w1+w1/2)-t_d,3*h/4+t_d], #  'LSL->SLL',
            [w/2,-t_d], #  'LLS->LSS',
            [w-(w1+w1/2)-t_d,h/4-t_d], #  'LLS->LSL',
            [w-w1/2+t_d,h/4-t_d], #  'LLL->LLS',
            [w+r_c/2,h/2-r_c/2-t_d]#  'LLL->LLL']
            ]
    
    # Vertical/horizontal alignments of edge labels
    edge_label_va = ['bottom','center','center','bottom','center','top','center',
                     'center','center','center','bottom','center','top','center',
                     'center','top']
    edge_label_ha = ['center','center','center','center','center','center','left',
                     'center','center','right','center','center','center','center',
                     'center','center']
    
    # Rotation angle of edge label text
    edge_label_rot = [0,45+a_t,-45-a_t,0,45+a_t,0,-90,-45-a_t,-45-a_t,90,0,
                      45+a_t,0,-45-a_t,45+a_t,0]
    
    if opts['show_edge_labels']:
        edge_labels = [str(round([j*100 for j in trans_obs][i],1)) for i in range(16)]
        
        for i in range(len(trans_obs)):
            
            # Correct inner loop annotations based on node size
            if (i == 5) or (i == 10):
                if opts['scale_nodes']:
                    inner_node_d = node_weights[5]-node_weights[2]
                    edge_lbl_offset = -inner_node_d/100
                else:
                    edge_lbl_offset = 0
            elif i==0:
                edge_lbl_offset = -sl_d_000
            elif i==15:
                edge_lbl_offset = sl_d_111
            else:
                edge_lbl_offset = 0
            
            if edge_default_labels[i][-1] == 'S':
                edge_lbl = 'S (' + edge_labels[i] + ')'
            else:
                edge_lbl = 'L (' + edge_labels[i] + ')'
            plt.annotate(edge_lbl,
                         [edge_label_locs[i][0]+edge_lbl_offset, edge_label_locs[i][1]],
                         ha=edge_label_ha[i],
                         va=edge_label_va[i],
                         rotation=edge_label_rot[i],
                         fontsize=edge_label_font_size,
                         color=edge_label_color)

    plt.xlim((-1.1*r_c-sl_d_000,w+1.1*r_c+sl_d_111))
    plt.ylim(-1.1*np.max([node_sizes[4], node_sizes[6]])/2000,
             h+1.4*np.max([node_sizes[1], node_sizes[3]])/3000)
    plt.axis('off')            
    
    if not opts['scale_edges']:
        sc = plt.scatter(np.zeros(16),np.zeros(16),s=np.zeros(8),c=edge_weights,cmap=cm)
    
    return sc
