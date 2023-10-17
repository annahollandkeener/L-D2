########################################## AESTHETICS ##########################################
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

monthLegend = [
    plt.Line2D([0], [0], marker='s', color='lightblue', label='January', markersize=15, linestyle='None'),
    plt.Line2D([0], [0], marker='s', color='#a5d6c5', label='February', markersize=15, linestyle='None'),
    plt.Line2D([0], [0], marker='s', color='#84ad89', label='March', markersize=15, linestyle='None'),
    plt.Line2D([0], [0], marker='s', color='#b0c27a', label='April', markersize=15, linestyle='None'),
    plt.Line2D([0], [0], marker='s', color='#f5f587', label='May', markersize=15, linestyle='None'),
    plt.Line2D([0], [0], marker='s', color='#e0b15a', label='June', markersize=15, linestyle='None'),
    plt.Line2D([0], [0], marker='s', color='#e89464', label='July', markersize=15, linestyle='None'),
    plt.Line2D([0], [0], marker='s', color='#b37659', label='August', markersize=15, linestyle='None'),
    plt.Line2D([0], [0], marker='s', color='#b06363', label='September', markersize=15, linestyle='None'),
    plt.Line2D([0], [0], marker='s', color='#f27c7c', label='October', markersize=15, linestyle='None'),
    plt.Line2D([0], [0], marker='s', color='#c086c4', label='November', markersize=15, linestyle='None'),
    plt.Line2D([0], [0], marker='s', color='#b6abcc', label='December', markersize=15, linestyle='None'),

]
def monthColors(plot):
    plt.axvspan(1, 31, facecolor='lightblue', alpha=0.5) #jan
    plt.axvspan(31, 60, facecolor="#a5d6c5", alpha=.5) #feb
    plt.axvspan(60, 91, facecolor="#84ad89", alpha=0.5) #mar
    plt.axvspan(91, 121, facecolor="#b0c27a", alpha=0.5) #apr
    plt.axvspan(121, 152, facecolor="#f5f587", alpha=0.5) #may
    plt.axvspan(152, 182, facecolor="#e0b15a", alpha=0.5) #jun
    plt.axvspan(182, 213, facecolor="#e89464", alpha=0.5) #jul
    plt.axvspan(213, 244, facecolor="#b37659", alpha=0.5) #aug
    plt.axvspan(244, 274, facecolor="#b06363", alpha=0.5) #sep
    plt.axvspan(274, 305, facecolor="#f27c7c", alpha=0.5) #oct
    plt.axvspan(305, 335, facecolor="#c086c4", alpha=0.5) #nov
    plt.axvspan(335, 366, facecolor="#b6abcc", alpha=0.5) #dec


defaultypos = [1500, 3500, 7500, 10000]  # Define the Y-axis tick positions
defaultylab = ['1500', '3500', '7500', '10000']  # Define the labels for the tick positions

xtick_positions = [1, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]  # Define the Y-axis tick positions
xtick_labels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']  # Define the labels for the tick positions