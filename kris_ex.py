#%% imports and functions
import matplotlib.pyplot as plt
import numpy as np

#%% data
atm_u = [6, 5, -10, -2]        # m/s   from 0 to 1000 hPa (ocean surface)
atm_q = [0.1, 2, 20, 25]       # g/kg
dp    = [200-0,600-200,900-600,1000-900]   # hPa

oce_u = [1, 0.2, -0.2, 0.05]   # m/s   from 0 to 4100 m depth  
oce_s = [34, 34, 33, 32]       # g/kg
oce_T = [25+273, 10+273, 9+273, 5+273]        # K
dz    = [100-0,1100-100,2100-1100,4100-2100] # m

cp_oce  =  4000  # J/kgK 
rho_oce =  1025  # kg/m3
cp_atm  =  1000  # J/kgK
rho_atm =  1.2   # kg/m3
L       =  2500  # J/g
lat     =  10    # degrees (Hadley, easterly winds)
oce_fr  =  0.7   # fraction of ocean surface
Rx      =  6371e3*np.cos(lat)*2*np.pi # m (horizontal length scale at lat=10)   

#%%  part 1:  overturning psi(z) for ocean
psi_o = [oce_u[i]*dz[i]*Rx*oce_fr for i in range(len(dz))]  
psi_o.insert(0, 0)  

#%% part 2: heat transport by the ocean
psi_h = [psi_o[1:][i]*rho_oce*cp_oce*oce_T[i] for i in range(len(dz))]
psi_h.insert(0, 0)  

#%% part 3: salinity transport by the ocean
psi_s = [psi_o[1:][i]*rho_oce*oce_s[i] for i in range(len(dz))]
psi_s.insert(0, 0)  

#%% part 4: overturning psi(p) for atmosphere
psi_a = [atm_u[i]*dp[i]*Rx/9.81 for i in range(len(dp))]  
psi_a.insert(0, 0)  

#%% part 5: latent heat transport by the atmosphere
psi_q = [psi_a[1:][i]*atm_q[i]*L for i in range(len(dp))]
psi_q.insert(0, 0)  


#%% visualise results
fig,axs = plt.subplots(1,2,figsize=(12,7))
axs[0].plot(psi_o, np.cumsum([0] + dz),
            color="k",label=r"$\psi_O$ ($m^3 s^{-1}$)")
axs[0].plot([p/1e9 for p in psi_h], np.cumsum([0] + dz),
            color="r",label=r"Heat tr. / 1e9 ($J s^{-1}$)")
axs[0].plot([p/1e5 for p in psi_s], np.cumsum([0] + dz),
            color="b",label=r"Salt tr. / 1e5 ($g s^{-1}$)")
axs[1].plot(psi_a, np.cumsum([0] + dp),
            color="k",label=r"$\psi_A$ ($kg s^{-1}$)")
axs[1].plot([p/1e5 for p in psi_q], np.cumsum([0] + dp),
            color="g",label=r"Latent heat tr. / 1e5 ($J s^{-1}$)")
axs[0].set_ylabel(r"Depth $z$ (m)")
axs[1].set_ylabel(r"Height $p$ (hPa)")
axs[0].set_title("Ocean")
axs[1].set_title("Atmosphere")
axs[0].set_xlim(left=-6e9,right=6e9)
axs[1].set_xlim(left=-1.1e10,right=1.1e10)
for ax in axs:
    ax.invert_yaxis()
    ax.axvline(x=0, color='k', ls='--', lw=0.7)
    ax.grid()
    ax.legend(loc="upper right")
    ax.set_xlabel(r"Streamfunctions and transport")
plt.gcf().savefig("/Users/lodo0477/Documents/PhD/Courses/General Circulation/Homeworks/Kristofer ex/stream_f.png", dpi=300, bbox_inches='tight')

# %%