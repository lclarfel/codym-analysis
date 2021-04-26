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

def draw_order_2(states_obs, states_order, trans_obs, trans_order, ax, opts):

    if 'edge_labels' not in opts:
        opts['edge_labels'] = trans_obs

    # GENERAL CHARACTERISTICS
    fig_dpi = 72
    h = 3 # Total vertical displacement
    w = 6 # Total horizontal displacement
    
    # NODE CHARACTERISTICS
    show_node_inlabels = True # Show node label inside node
    node_lbl_size = 14 # Fot size of label inside node
    node_font_color = 'w' # Font color of label inside node
    d_n = 0.45 # How much to displace node label (i.e., more if node is bigger)
    node_edge_width = 2
    node_default_size = 700 # If not scaling nodes

    # EDGE CHARACTERISTICS
    edge_label_font_size = 14
    edge_label_color = 'k'
    r_c =  h/2 # Radius for self-loop circles
    d_inner = 0.17 # Vertical displacement of inner-loop arrows from center
    a_c = 5 # Extra displacement prevents self-loop arc from overlapping arrowhead
    max_edge_width = 8
    min_edge_width = 2    
    edge_width = 2.5 # Width of self-loop lines
    inner_arc_rad = 0.5
    inner_arc = "arc3,rad=" + str(inner_arc_rad) # "Connection Style", size of arc on inner-loop
    non_sig_style = '--' # 'simple,tail_width=1.5,head_width=6,head_length=8' # If no significance, fill the arrowheads
    sig_style = '-' # 'simple,tail_width=1.5,head_width=6,head_length=8'
    se_d = 0.3 # straight-edge displacement
    il_el_d= 1.1 # inner-loop, edge label displacement
    
    # Edge label characteristics
    a_t = -18 # Adjust edge label angles by this amount
    t_d = 0.2 # text displacement for edge labels 
    a_d = 24 # Displacement of inner edges (in degrees)
    el_d = 0.5 # Displacement of edge lables for self-loops
    il_d = 0.1 # Some extra horizontal displacement for the inner loop edge labels
    
    # Node order (for plotting)
    states_all = np.array([[0., 0.],
                           [0., 1.],
                           [1., 0.],
                           [1., 1.]])
    
    # Edge order (for plotting)
    transition_all =  np.array([[0., 0., 0., 0.],
                                [0., 0., 0., 1.],
                                [0., 1., 1., 0.],
                                [0., 1., 1., 1.],
                                [1., 0., 0., 0.],
                                [1., 0., 0., 1.],
                                [1., 1., 1., 0.],
                                [1., 1., 1., 1.]])
    
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
    
    # Fil in any missing TRANSITIONS w/ zeros and fix the ordering
    temp_trans = []
    temp_is_sig = []
    temp_trans_lbls = []
    for trans in transition_all:
        
        i_trans = np.where(np.all(trans_order==trans,axis=1))[0] # matching index from observed data
        if len(i_trans):
            temp_trans.append(trans_obs[i_trans[0]])
            temp_is_sig.append(opts['is_sig_trans'][i_trans[0]])
            temp_trans_lbls.append(opts['edge_labels'][i_trans[0]])
        else:
            temp_trans.append(0)
            temp_is_sig.append(True)
    trans_obs = temp_trans
    opts['is_sig'] = temp_is_sig
    opts['edge_labels'] = temp_trans_lbls
    trans_order = np.array([np.hstack((x[:3], x[3:])) for x in transition_all])
        
    #><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><
    # 
    #><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><#><
    
    # convert frequencies to percents to use as weights
    node_weights = np.array(states_obs)*100 # States_obs is defined in fig_poopulated_model.py, will be an input variable
    edge_weights = np.array(trans_obs)*100     
    
    # Convert weights to strings for labelling
    node_labels = [str(round(nw,1)) for nw in node_weights] # NOTE, 1 sig fig
    
    #>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-
    #>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-<#>-
            
    # Edges that are NOT curvy (i.e., excluding 000->0, 111->1, 101->0, and 010->1)
    E_straight = np.array([[0,1],[1,3],[3,2],[2,0]]) 
    E_straight_i = [1,3,6,4] # Matching indexes to get from E_straight to E (for adding weights)
    node_lbls = ['SS','SL','LS','LL']
    
    # Node positions
    node_pos = [[] for _ in range(4)]
    node_pos[0] = [0,h/2]
    node_pos[1] = [w/2,h]
    node_pos[2] = [w/2,0]
    node_pos[3] = [w,h/2]
    
    # Figure initialization
    ax = plt.gca()    
    
    # Plot the nodes
    node_pos_arr = np.array(node_pos) # Get into good numpy format
    cm = plt.cm.get_cmap(opts['colormap']) # Set the colormap
    
    # Establish min/max size for nodes (if scaled)
    if opts['scale_nodes']:
        node_min_size = 500
        node_max_size = 1500
        
        # This is as big/small as a node can get, based on the weight
        if 'w_range_nodes' in opts:
            w_range = opts['w_range_nodes']
        max_weight_adj = (np.abs(w_range[1])+1)**1.8*9.2 # heuristic works well
        if w_range[0] >= 0:
            min_weight_adj = (np.abs(w_range[0])+1)**1.8*9.2
        else:
            min_weight_adj = 0
        
        node_sizes = (np.abs(node_weights)+1)**1.8*9.2 # Heuristic has worked well for node sizing
        node_sizes = (node_sizes-min_weight_adj)/(max_weight_adj-min_weight_adj) # This normalizes into a scale of [0,1] based on w_range
        node_sizes = node_sizes*(node_max_size-node_min_size) + node_min_size
    else:
        node_sizes = np.ones(4)*node_default_size
    
    sl_d_00 = np.sqrt(node_sizes[0])**0.8/50 # Additional offset for 00-loop, by node size
    sl_d_11 = np.sqrt(node_sizes[3])**0.8/50 # Additional offset for 11-loop, by node size
    
    # Plot the nodes
    for jj in range(4):
        if 'is_sig_nodes' in opts:
            if opts['is_sig_nodes'][jj]:
                sig_color = 'k'
            else:
                sig_color = 'gray'
        else:
            sig_color = 'k'
    
        plt.scatter(node_pos_arr[jj,0],node_pos_arr[jj,1],s=node_sizes[jj],c=sig_color,linewidth=node_edge_width,cmap=cm,zorder=3)


    if 'w_range_edges' in opts:
        w_range = opts['w_range_edges']
    
    sc = plt.scatter(np.zeros(8),np.zeros(8),s=np.zeros(8),c=edge_weights,cmap=cm)
    plt.clim(w_range[0], w_range[1]) # Set max/min limits for the colorbar
    
    for i in range(4):
        if show_node_inlabels:
            plt.annotate(node_lbls[i],[node_pos[i][0],node_pos[i][1]],ha='center',va='center',color=node_font_color,weight='bold',fontsize=node_lbl_size)
        
    # Plot all of the straight-line edges (including offsets for node size)
    for i in range(len(E_straight)):
    
        nodes = E_straight[i] # Get TO and FROM nodes for the straight edge
        
        color_i = (edge_weights[E_straight_i[i]]-w_range[0])/(w_range[1]-w_range[0])
        if 'is_sig_trans' in opts:
            if opts['is_sig_trans'][E_straight_i[i]]:
                ls = sig_style
            else:
                ls = non_sig_style
        else:
            ls = sig_style
        
        if opts['scale_edges']:
            ew = (np.abs(edge_weights[E_straight_i[i]])-0)/(w_range[1]-0)*(max_edge_width-min_edge_width)+min_edge_width
        else:
            ew = edge_width
            
        inv = ax.transData.inverted()
        rpix_r_from = node_sizes[nodes[0]]**0.5/2*fig_dpi/72
        act_r_from = inv.transform([rpix_r_from,rpix_r_from])-inv.transform([0,0])
    
        rpix_r_to = node_sizes[nodes[1]]**0.5/2*fig_dpi/72
        act_r_to = inv.transform([rpix_r_to,rpix_r_to])-inv.transform([0,0])
        
        # Extra dispalcement based on line width
        rpix_r_e = ew/2*fig_dpi/72
        act_r_e = inv.transform([rpix_r_e,rpix_r_e])-inv.transform([0,0])
    
        edge_color = cm(color_i)
        style_s ="Simple,tail_width=1.5,head_width=" + str(ew*1.3) + ",head_length=" + str(ew*1.3*1.25)
        
        if i == 0:
            plt.plot([node_pos[nodes[0]][0]+(act_r_from[0]+act_r_e[0]+se_d)/np.sqrt(2),
                      node_pos[nodes[1]][0]-(act_r_to[0]+act_r_e[0]+se_d)/np.sqrt(2)],
                      [node_pos[nodes[0]][1]+(act_r_from[1]+act_r_e[1]+se_d)/np.sqrt(2),
                        node_pos[nodes[1]][1]-(act_r_to[1]+act_r_e[1]+se_d)/np.sqrt(2)],
                      linestyle=ls,color = cm(color_i),linewidth=ew,zorder=3) 

            slope = (
                (node_pos[nodes[1]][1]-(act_r_to[1]+act_r_e[1]+se_d)/np.sqrt(2)) -
                (node_pos[nodes[0]][1]+(act_r_from[1]+act_r_e[1]+se_d)/np.sqrt(2))
                ) / (
                (node_pos[nodes[1]][0]-(act_r_to[0]+act_r_e[0]+se_d)/np.sqrt(2)) -
                (node_pos[nodes[0]][0]+(act_r_from[0]+act_r_e[0]+se_d)/np.sqrt(2)))

            a = patches.FancyArrowPatch([node_pos[nodes[1]][0]-(act_r_to[0]+act_r_e[0]+se_d)/np.sqrt(2), 
                                          node_pos[nodes[1]][1]-(act_r_to[1]+act_r_e[1]+se_d)/np.sqrt(2)], 
                                        [node_pos[nodes[1]][0]-(act_r_to[0]+act_r_e[0]+se_d)/np.sqrt(2)+(0.05+act_r_e[1])/slope,
                                          node_pos[nodes[1]][1]-(act_r_to[1]+act_r_e[1]+se_d)/np.sqrt(2)+(0.05+act_r_e[1])],
                                        color=cm(color_i),linewidth=ew,arrowstyle=style_s)
            
        elif (i == 1):            
            plt.plot([node_pos[nodes[0]][0]+(act_r_from[0]+act_r_e[0]+se_d)/np.sqrt(2),
                      node_pos[nodes[1]][0]-(act_r_to[0]+act_r_e[0]+se_d)/np.sqrt(2)],
                      [node_pos[nodes[0]][1]-(act_r_from[1]+act_r_e[1]+se_d)/np.sqrt(2),
                        node_pos[nodes[1]][1]+(act_r_to[1]+act_r_e[1]+se_d)/np.sqrt(2)],
                      linestyle=ls,color = edge_color,linewidth=ew,zorder=3) 
            
            slope = (
                (node_pos[nodes[1]][1]+(act_r_to[1]+act_r_e[1]+se_d)/np.sqrt(2)) -
                (node_pos[nodes[0]][1]-(act_r_from[1]+act_r_e[1]+se_d)/np.sqrt(2))
                ) / (
                (node_pos[nodes[1]][0]-(act_r_to[0]+act_r_e[0]+se_d)/np.sqrt(2)) -
                (node_pos[nodes[0]][0]+(act_r_from[0]+act_r_e[0]+se_d)/np.sqrt(2)))
            
            a = patches.FancyArrowPatch([node_pos[nodes[1]][0]-(act_r_to[0]+act_r_e[0]+se_d)/np.sqrt(2),
                                          node_pos[nodes[1]][1]+(act_r_to[1]+act_r_e[1]+se_d)/np.sqrt(2)],
                                        [node_pos[nodes[1]][0]-(act_r_to[0]+act_r_e[0]+se_d)/np.sqrt(2)-(0.05+act_r_e[1])/slope,
                                          node_pos[nodes[1]][1]+(act_r_to[1]+act_r_e[1]+se_d)/np.sqrt(2)-(0.05+act_r_e[1])],
                                        color=edge_color,linewidth=ew,arrowstyle=style_s)

        elif (i == 2):
            plt.plot([node_pos[nodes[0]][0]-(act_r_from[0]+act_r_e[0]+se_d)/np.sqrt(2),
                      node_pos[nodes[1]][0]+(act_r_to[0]+act_r_e[0]+se_d)/np.sqrt(2)],
                      [node_pos[nodes[0]][1]-(act_r_from[1]+act_r_e[1]+se_d)/np.sqrt(2),
                        node_pos[nodes[1]][1]+(act_r_to[1]+act_r_e[1]+se_d)/np.sqrt(2)],
                      linestyle=ls,color = edge_color,linewidth=ew,zorder=3)         
            
            slope = (
                (node_pos[nodes[1]][1]+(act_r_to[1]+act_r_e[1]+se_d)/np.sqrt(2)) -
                (node_pos[nodes[0]][1]-(act_r_from[1]+act_r_e[1]+se_d)/np.sqrt(2))
                ) / (
                (node_pos[nodes[1]][0]+(act_r_to[0]+act_r_e[0]+se_d)/np.sqrt(2)) -
                (node_pos[nodes[0]][0]-(act_r_from[0]+act_r_e[0]+se_d)/np.sqrt(2)))
            
            a = patches.FancyArrowPatch([node_pos[nodes[1]][0]+(act_r_to[0]+act_r_e[0]+se_d)/np.sqrt(2),
                                         node_pos[nodes[1]][1]+(act_r_to[1]+act_r_e[1]+se_d)/np.sqrt(2)],
                                        [node_pos[nodes[1]][0]+(act_r_to[0]+act_r_e[0]+se_d)/np.sqrt(2)-0.05/slope,
                                         node_pos[nodes[1]][1]+(act_r_to[1]+act_r_e[1]+se_d)/np.sqrt(2)-0.05],
                                        color=edge_color,linewidth=ew,arrowstyle=style_s)
    
        elif (i == 3):  
            plt.plot([node_pos[nodes[0]][0]-(act_r_from[0]+act_r_e[0]+se_d)/np.sqrt(2),
                      node_pos[nodes[1]][0]+(act_r_to[0]+act_r_e[0]+se_d)/np.sqrt(2)],
                      [node_pos[nodes[0]][1]+(act_r_from[1]+act_r_e[1]+se_d)/np.sqrt(2),
                        node_pos[nodes[1]][1]-(act_r_to[1]+act_r_e[1]+se_d)/np.sqrt(2)],
                      linestyle=ls,color = edge_color,linewidth=ew,zorder=3)     
            
            slope = (
                (node_pos[nodes[1]][1]-(act_r_to[1]+act_r_e[1]+se_d)/np.sqrt(2)) -
                (node_pos[nodes[0]][1]+(act_r_from[1]+act_r_e[1]+se_d)/np.sqrt(2))
                ) / (
                (node_pos[nodes[1]][0]+(act_r_to[0]+act_r_e[0]+se_d)/np.sqrt(2)) -
                (node_pos[nodes[0]][0]-(act_r_from[0]+act_r_e[0]+se_d)/np.sqrt(2)))
            
            a = patches.FancyArrowPatch([node_pos[nodes[1]][0]+(act_r_to[0]+act_r_e[0]+se_d)/np.sqrt(2),
                                         node_pos[nodes[1]][1]-(act_r_to[1]+act_r_e[1]+se_d)/np.sqrt(2)],
                                        [node_pos[nodes[1]][0]+(act_r_to[0]+act_r_e[0]+se_d)/np.sqrt(2)+0.05/slope,
                                         node_pos[nodes[1]][1]-(act_r_to[1]+act_r_e[1]+se_d)/np.sqrt(2)+0.05],
                                        color=edge_color,linewidth=ew,arrowstyle=style_s)
    
            
        ax.add_patch(a) # Add the arrow to the plot
    
    # Self-loop edges (without arrowheads)
    if opts['scale_edges']:
        color_i = (edge_weights[0]-w_range[0])/(w_range[1]-w_range[0])
        c = cm(color_i)
        ew = (np.abs(edge_weights[0])-0)/(w_range[1]-0)*(max_edge_width-min_edge_width)+min_edge_width    
    else:
        c = edge_label_color
        ew = edge_width
        
    if opts['is_sig'][0]:
        ls = sig_style
    else:
        ls = non_sig_style
    
    p1 = patches.Arc([-r_c/2-sl_d_00,h/2], r_c, r_c, angle=0.0, theta1 = a_d + a_c, theta2 = 360 - a_d,linewidth=ew,color = c,linestyle=ls)
    
    
    if opts['scale_edges']:
        color_i = (edge_weights[7]-w_range[0])/(w_range[1]-w_range[0])
        c = cm(color_i)
        ew = (np.abs(edge_weights[7])-0)/(w_range[1]-0)*(max_edge_width-min_edge_width)+min_edge_width
    else:
        c = edge_label_color
        ew = edge_width
        
    if opts['is_sig'][7]:
        ls = sig_style
    else:
        ls = non_sig_style
    
    p2 = patches.Arc([w+r_c/2+sl_d_11,h/2], r_c, r_c, angle=0.0, theta1 = 180+a_d + a_c, theta2 = 180 - a_d,linewidth=ew,color = c,linestyle=ls)
    
    # Trying to fix arrows
    d_e_inner_U = np.sqrt(node_sizes[1])**0.8/45 # node_weights[2]/50
    d_e_inner_D = np.sqrt(node_sizes[2])**0.8/45 # node_weights[5]/50
    
    
    if opts['scale_edges']:
        color_i = (edge_weights[5]-w_range[0])/(w_range[1]-w_range[0])
        c = cm(color_i)
        ew = (np.abs(edge_weights[5])-0)/(w_range[1]-0)*(max_edge_width-min_edge_width)+min_edge_width
    else:
        c = edge_label_color
        ew = edge_width
        
    if opts['is_sig'][5]:
        ls = sig_style
    else:
        ls = non_sig_style

    style_10_1="Simple,tail_width=1.5,head_width=" + str(min([ew,7])*2) + ",head_length=" + str(min([ew,7])*2*1.25)
    p3 = patches.FancyArrowPatch([w/2+il_d+0.05,h-d_inner-d_e_inner_U-0.05],[w/2+il_d,h-d_inner-d_e_inner_U],color = c,linewidth=ew,arrowstyle = style_10_1) # connectionstyle=inner_arc
    
    # Define coordinates for 01->0 edge
    y1 = [w/2+il_d, d_inner+d_e_inner_D]
    x1 = [w/2+il_d,h-d_inner-d_e_inner_U]
    
    ax.annotate("",
                xy=(x1[0], x1[1]), xycoords='data',
                xytext=(y1[0], y1[1]), textcoords='data',
                arrowprops=dict(arrowstyle="-", color=c, 
                                shrinkA=5, shrinkB=5,
                                patchA=None, patchB=None,
                                connectionstyle=inner_arc,
                                linestyle=ls,
                                linewidth=ew)
                )
    
    if opts['scale_edges']:
        color_i = (edge_weights[2]-w_range[0])/(w_range[1]-w_range[0])
        c = cm(color_i)
        ew = (np.abs(edge_weights[2])-0)/(w_range[1]-0)*(max_edge_width-min_edge_width)+min_edge_width
    else:
        c = edge_label_color
        ew = edge_width
        
    if opts['is_sig'][2]:
        ls = sig_style
    
    else:
        ls = non_sig_style
    
    style_01_0="Simple,tail_width=1.5,head_width=" + str(min([ew,7])*2) + ",head_length=" + str(min([ew,7])*2*1.25)

    p4 = patches.FancyArrowPatch([w/2-il_d-0.05,d_inner+d_e_inner_D+0.15],[w/2-il_d,d_inner+d_e_inner_D],connectionstyle=inner_arc,color = c,linewidth=ew,arrowstyle = style_01_0)    
    
    y1 = [w/2-il_d, h-d_inner-d_e_inner_D]
    x1 = [w/2-il_d,d_inner+d_e_inner_D]
    ax.annotate("",
                xy=(x1[0], x1[1]), xycoords='data',
                xytext=(y1[0], y1[1]), textcoords='data',
                arrowprops=dict(arrowstyle="-", color=c,
                                shrinkA=5, shrinkB=5,
                                patchA=None, patchB=None,
                                connectionstyle=inner_arc,
                                linestyle=ls,
                                linewidth=ew)
                )
    
    ax.add_patch(p1)
    ax.add_patch(p2)
    
    ax.add_patch(p3)
    ax.add_patch(p4)
    
    theta = np.deg2rad(a_d)
    yy = r_c * np.sin(theta)
    xx = r_c - r_c * np.cos(theta)
    d_yy = r_c * np.sin(theta-.001)
    d_xx = r_c - r_c * np.cos(theta-.001)
    
    if opts['scale_edges']:
        color_i = (edge_weights[0]-w_range[0])/(w_range[1]-w_range[0])
        c = cm(color_i)
        ew = (np.abs(edge_weights[0])-0)/(w_range[1]-0)*(max_edge_width-min_edge_width)+min_edge_width
    else:
        c = edge_label_color
        ew = edge_width
    
    style_00_0="Simple,tail_width=1.5,head_width=" + str(min([ew,7])*2) + ",head_length=" + str(min([ew,7])*2*1.25)
    p5= patches.FancyArrowPatch([-xx/2-sl_d_00,h/2+yy/2],[-d_xx/2-sl_d_00,h/2+d_yy/2],color = c,linewidth=ew, arrowstyle = style_00_0)
    
    yy = -r_c * np.sin(theta)
    xx = r_c - r_c * np.cos(theta)
    d_yy = -r_c * np.sin(theta-.001)
    d_xx = r_c - r_c * np.cos(theta-.001)
    
    if opts['scale_edges']:
        color_i = (edge_weights[7]-w_range[0])/(w_range[1]-w_range[0])
        c = cm(color_i)
        ew = (np.abs(edge_weights[7])-0)/(w_range[1]-0)*(max_edge_width-min_edge_width)+min_edge_width
    else:
        c = edge_label_color
        ew = edge_width
    
    if opts['is_sig'][7]:
        ls = sig_style
    else:
        ls = non_sig_style
    
    style_11_1="Simple,tail_width=1.5,head_width=" + str(min([ew,7])*2) + ",head_length=" + str(min([ew,7])*2*1.25)
    p6= patches.FancyArrowPatch([w+xx/2+sl_d_11,h/2+yy/2],[w+d_xx/2+sl_d_11,h/2+d_yy/2],color = c,linewidth=ew, arrowstyle = style_11_1)
    ax.add_patch(p5)
    ax.add_patch(p6)
    
    sl_d_00_2 = np.sqrt(node_sizes[0])**0.8/12 # Additional offset for 00-loop, by node size
    sl_d_11_2 = np.sqrt(node_sizes[0])**0.8/12 # Additional offset for 11-loop, by node size
    
    node_label_loc = [[-sl_d_00_2,h/2],
                      [w/2,h+d_n],
                      [w/2,-d_n],
                      [w+sl_d_11_2,h/2]]
    
    node_label_va = ['center' for _ in range(4)]
    node_label_ha = ['left','center','center','right']
    
    if opts['show_node_labels']:
        for i in range(4):
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
                         fontsize = node_lbl_size)
        
    states_obs = np.arange(4)+1/np.sum(np.arange(4)+1)
    states_order = np.array([[0., 0.],
                             [0., 1.],
                             [1., 0.],
                             [1., 1.]])
    
    trans_order =  np.array([[0., 0., 0., 0.],
                                  [0., 0., 0., 1.],
                                  [0., 1., 1., 0.],
                                  [0., 1., 1., 1.],
                                  [1., 0., 0., 0.],
                                  [1., 0., 0., 1.],
                                  [1., 1., 1., 0.],
                                  [1., 1., 1., 1.]])
    
    edge_label_locs = [
            [-r_c/2-el_d/2,h/2+r_c/2+el_d/2], # '00->00',
            [w/4-t_d,3*h/4+t_d], #  '00->01',
            [w/2-il_el_d,h/2], #  '01->10', 
            [3*w/4+t_d,3*h/4+t_d], #  '01->11',
            [w/4-t_d,h/4-t_d], #  '10->00',
            [w/2+il_el_d,h/2], #  '10->01',
            [3*w/4+t_d,h/4-t_d], #  '11->10',
            [w+r_c/2+el_d/2,h/2-r_c/2-el_d/2] #  '11->11'
    ]

    # Vertical/horizontal alignments of edge labels
    edge_label_va = ['center','center','center','center','center','center','center',
                     'center']
    edge_label_ha = ['center','center','center','center','center','center','center',
                     'center']
    
    # Rotation angle of edge label text
    edge_label_rot = [0, 45+a_t, -90, -45-a_t, -45-a_t, 90, 45+a_t, 0]
    
    if opts['show_edge_labels']:
        edge_labels = [str(round([j*100 for j in opts['edge_labels']][i],1)) for i in range(8)]
        
        for i in range(len(trans_obs)):
                
            if transition_all[i][-1] == 0:
                extra_bit = 'S ('
            else:
                extra_bit = 'L ('
            plt.annotate(extra_bit+edge_labels[i]+')',
                         [edge_label_locs[i][0], edge_label_locs[i][1]],
                         ha=edge_label_ha[i],
                         va=edge_label_va[i],
                         rotation=edge_label_rot[i],
                         fontsize=edge_label_font_size,
                         color=edge_label_color)
    
    plt.xlim((-1.1*r_c-sl_d_00-el_d/2,w+1.1*r_c+sl_d_11+el_d/2))
    plt.ylim(-1.1*node_sizes[2]/2000-d_n/2,
              h+1.1*node_sizes[1]/3000+d_n/2)
    plt.axis('off')
    
    return sc
