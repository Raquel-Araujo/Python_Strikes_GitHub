#!/usr/bin/python
# -*- coding: utf-8 -*-
### estas duas linhas de cima faz reconher acentos do portugues

### bibliotecas
import matplotlib.pyplot as plt
import glob
import matplotlib.image as mpimg 
import matplotlib.gridspec as gridspec


#################################
# funcao


# def make_mult_fig(img, size, grid, output, date, nomestrike):
def make_mult_fig(img, size, grid, output, date, nomestrike, imgextent, strike, gapstrike, dateimg):

    #################################################################################################################################################################################
    ### make all figures together
    #########################################################################
    ### define a fonte da letras
    plt.rcParams["font.family"] = "Times New Roman"
    #########################################################################
    ### letras, caso o numero de subdivisoes seja maior que 6, aumentar a quantidade de letras

    abcd = ["a", "b" , "c" ,"d", "e", "f","g", "h" , "i" ,"j", "k", "l"]
    ### define o tamanho da figura
    fig = plt.figure(figsize=(size[0],size[1]))
    #########################################################################
    # gridspec inside gridspec
    outer_grid = gridspec.GridSpec(grid[0], grid[1], wspace=0.02, hspace=-0.2)
    #########################################################################

    ### plot each image in subplot. i is each panel
    for i in range(grid[0]*grid[1]):
        ax = plt.Subplot(fig, outer_grid[i])
        ax.imshow(img[i], extent=imgextent)
        strike.plot(ax=ax, facecolor='r', edgecolor='r', markersize=10)
        if any(gapstrike.date == dateimg[i]):
            gapsel = gapstrike.loc[gapstrike.date==dateimg[i]]
            gapsel.plot(ax=ax, facecolor='none', edgecolor='r',linewidth=0.7)
        ax.set_xticks([])
        ax.set_yticks([])
        #######
        ## plot letter a b c d 
        # print(str(date[i]))
        ax.text(0.05, 0.08, str(date[i]), transform=ax.transAxes, size=10, bbox=dict(facecolor='white'))
        ax.text(0.05, 0.88, abcd[i], transform=ax.transAxes, size=10, bbox=dict(facecolor='white'))

    
        fig.add_subplot(ax)


    # remove all spines
    all_axes = fig.get_axes()
    for ax in all_axes:
        for sp in ax.spines.values():
            sp.set_visible(False)
    fig.suptitle(nomestrike)
    fig.subplots_adjust(top=0.95)
    # fig.set_tight_layout(True)
    #######################
    ### save on disk
    plt.savefig(output, dpi=500, bbox_inches='tight')
    plt.close('all')
    #################################################################################################################################################################################
