import topas2numpy as t2np
import numpy as np
import matplotlib.pyplot as plt


cyl1 = t2np.BinnedResult("PDDCylinder_2.csv")

depth = np.flip(cyl1.dimensions[2].get_bin_centers())
dose = np.squeeze(cyl1.data["Mean"])/np.max(cyl1.data["Mean"])

poly_order = np.array([2,4,6,8])
y_fit = np.zeros([len(poly_order)])
y_fit_data = np.zeros([len(poly_order)])

legend = len(poly_order) * [0]


fig4, ax = plt.subplots()
for i in range(len(poly_order)):

    y_coeffs = np.polyfit(depth,y,poly_order[i])
    y_fit = np.poly1d(y_coeffs)

    y_fit_data[i] = y_fit(zs)

    legend = str('%.d order polyfit' % (len(y_coeffs)-1))

    ax.plot(zs,y_fit_data[i],label=legend)


plt.figure(1)
plt.plot(depth, dose)
plt.xlabel('Depth (cm)')