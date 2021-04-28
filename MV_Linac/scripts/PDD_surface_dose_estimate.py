
import topas2numpy as t2np
import numpy as np
import matplotlib.pyplot as plt

#energies = ['tar_pcol','tar_pcol_scol','tar_pcol_scol_ff','tar_pcol_scol_ff_monchamb']

cyl1 = t2np.BinnedResult("PDDCyl_6.0MV_%s.csv" % energies[3])

depth = np.flip(cyl1.dimensions[2].get_bin_centers())
dose = np.squeeze(cyl1.data["Mean"])/np.max(cyl1.data["Mean"])

depth_fit = depth[574:]
dose_fit = dose[574:]

poly_order = np.arange(2,12,2)
y_fit = np.zeros([len(poly_order)])
y_fit_data = np.zeros([len(poly_order),len(depth_fit)])

legend = len(poly_order) * [0]

fig1, ax = plt.subplots()
for i in range(len(poly_order)):

    y_coeffs = np.polyfit(depth_fit,dose_fit,poly_order[i])
    y_fit = np.poly1d(y_coeffs)

    y_fit_data[i] = y_fit(depth_fit)

    legend = str('%.d order polyfit' % (len(y_coeffs)-1))

    plt.plot(depth_fit,y_fit_data[i],label=legend)

ax.set_xlabel('Depth (cm)')
plt.legend()

ax.plot(depth_fit,dose_fit,'k', label='Simulated')




# Using 6th order poly
y_coeffs = np.polyfit(depth_fit,dose_fit,6)
y_fit = np.poly1d(y_coeffs)

zero_y_fit = y_fit(0) * 100

build_up_depths = np.linspace(0,0.6,1000)
build_up_fit_dose = y_fit(build_up_depths)

print('Surface %% dose estimate: %.2f %%' % zero_y_fit)


data = np.genfromtxt('ChrisOBrien_Linac_Data.csv',delimiter=',')

equiv_square_size = 10

exp_depths = np.arange(0,30.5,0.5)
exp_pdd_10x10 = np.squeeze(data[1:,np.where(data[0]==equiv_square_size)[0]]/100)
exp_pdd_10x10_d10_norm = exp_pdd_10x10  / exp_pdd_10x10[np.where(exp_depths==10)]


fig2,ax = plt.subplots()
ax.plot(build_up_depths,build_up_fit_dose)
ax.plot(exp_depths, exp_pdd_10x10)
ax.set_xlim([0,1])


plt.show()