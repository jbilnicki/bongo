# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 10:07:02 2024

@author: MSI
"""



#import matplotlib.pyplot as plt
import voltammetry



file = voltammetry.open_data("hdcv_excel.xlsx")

current = file.loc[:,270]

voltammetry.analyze_transients(current, 2)

'''
subtracted = voltammetry.calculate_background_subtraction(file, bg=30)


#voltammetry.draw_heatmap(subtracted)
#voltammetry.draw_cv_plot(subtracted, 65, True)
sdbr = voltammetry.calculate_sdbr(file,bg=30)

plt.figure()
voltammetry.draw_cv_plot(sdbr, 65, True)
plt.savefig("cv.png",bbox_inches='tight')

'''

"""
import neuroanatomy


hemisphere = "left"
our_sample_image = "img/Nac_example.png"
anterior_posterior = 1.8

neuroanatomy.check_NAc(our_sample_image, anterior_posterior, hemisphere)


hemisphere = "left"
our_sample_image = "img/Nac_example.png"
anterior_posterior = 4.9

neuroanatomy.check_VTA(our_sample_image, anterior_posterior, hemisphere)
"""

