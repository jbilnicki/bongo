# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 10:07:02 2024

@author: MSI
"""



#import matplotlib.pyplot as plt
#import voltammetry


import photometry

file = photometry.open_file("~/Desktop/example.csv")

cs_1 = file["DeltaF/F-1"]

peak = photometry.normalize_peak(cs_1)

print(f'Normalized value of your peak is: {peak}')

auc = photometry.normalize_auc(cs_1)
print(auc)


'''
file = voltammetry.open_data("hdcv_excel.xlsx")

current = file.loc[:,270]

transients = voltammetry.analyze_transients(current, 0.5)
print(f'transients: {transients}')


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

