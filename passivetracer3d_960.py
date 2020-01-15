import h5py
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
outputDir = "/run/user/1000/gvfs/sftp:host=lisa.surfsara.nl,user=alaik/home/alaik/uw_py3_3D/t3d_960_llr_IW_nm/"

# fH = open(outputDir + "/checkpoint.log", "r")
#
# with open(outputDir + "/checkpoint.log", "r") as infile, open(
#     outputDir + "/tRcheckpoint.log", "w+"
# ) as outfile:
#     temp = infile.read().replace(";", "")
#     outfile.write(temp)
X, Z = np.meshgrid(
    np.linspace(
        0,
        12,
        33,
    ),
    np.linspace(
        0,
        12,
        33,
    ),
    indexing="ij",
)

time = np.genfromtxt(outputDir + "/tcheckpoint.log", delimiter=",")

for i in time[:, 0]:
    stStr = str(int(i)).zfill(5)
    with h5py.File(outputDir + "tswarm-" + stStr + ".h5", "r") as f:
        tcord = f["data"][()]
    with h5py.File(outputDir + "tvel-" + stStr + ".h5", "r") as f:
        tvel = f["data"][()]
    with h5py.File(outputDir + "tcoords-" + stStr + ".h5", "r") as f:
        ic = f["data"][()]

    crX = tcord[:, 0]
    crZ = tcord[:, 2]


    inX = ic[:, 0]
    inZ = ic[:, 2]
    width = .75
    hz = np.zeros_like(inX)
    matC = np.zeros_like(inX)
    matC[:] = 0
    hz[:] = -1
    gX = np.where(np.abs(np.cos(np.pi*inX)) > .95)
    gZ = np.where(np.abs(np.cos(np.pi*inZ)) > .95)

    mat = np.where((inZ < 2.0*3) & (inX > 0.3*3))
    slabF = np.where((inZ <= 2.0*3) & (inX <= 2.0*3) & (inX >= 0.3*3))
    overF = np.where((inZ <= 2.0*3) & (inX >= 2.0*3))
    indeF = np.where((inZ <= 1.0*3) & (inZ >= 0.2*3)
                     & (inX <= (0.85+0.3)*3) & (inX >= 0.3*3))
    ovfaF = np.where((inZ <= 2.0*3) & (inX >= 2.0*3) & (inX <= (2.0+0.075)*3))
    ovbaF = np.where((inZ <= 2.0*3) & (inX >= (2.0+0.075)*3)
                     & (inX <= (2.0+0.25)*3))
    hz[gX] = 1
    hz[gZ] = 1
    matC[slabF] = 11
    matC[indeF] = 3
    matC[overF] = 1
    matC[ovfaF] = 7
    matC[ovbaF] = 5
    hatch = (((np.round(inZ/width) % 2)+(np.round(inX/width) % 2)))
    # gXX = (np.cos(np.pi*inX) > .9)
    # gZZ = (np.cos(np.pi*inZ) > .9)
    # g = np.where(gXX | gZZ)
    g = 9
    # plt.plot(hatch)
    print("int...")
    Vx=interpolate.griddata((crZ, crX),tvel[:,0], (Z, X), method='nearest')
    Vz=interpolate.griddata((crZ, crX),tvel[:,2], (Z, X), method='nearest')
    Vm=(Vz**2 + Vx**2)**.5
    print("int")
    def plot_it():
        plt.clf()
        plt.xlim((0, 12))
        plt.ylim((0, 12))
        # plt.scatter(crZ, crX, c=hatch, s=12, marker='.',
        #             cmap='BrBG', alpha=0.8)


        plt.scatter(crZ[gX], crX[gX], c='black', s=12, alpha=0.5)
        plt.scatter(crZ[gZ], crX[gZ], c='black', s=12, alpha=0.5)
        plt.scatter(crZ[mat], crX[mat], c=matC[mat],s=24, cmap="tab20c")
        # plt.streamplot(Z,X,Vz,Vx, color=Vm,density = 2.5)
        q=plt.quiver(Z, X, Vz,Vx,Vm,scale=0.018, cmap='Greys')

        qk = plt.quiverkey(q, 0.9, 0.9, 0.0021928896839249795/2, r'$5 \frac{cm}{year}$', labelpos='E',
                   coordinates='figure')
                   # (tvel[:, 1]**2 + tvel[:, 0]**2)*.5, cmap='magma')
        #
        plt.gcf().set_size_inches(12, 12)
        plt.savefig('960/q'+stStr+".png", dpi=120)

    plot_it()

#
# #
# # %matplotlib
# plt.plot(10*np.sin(np.pi*2*inX))
#
# def plot_it():
#     plt.scatter(crX, crZ, c=hatch, s=5,marker="o")
#     plt.gcf().set_size_inches(10, 10)
#     plt.xlim((0, 12))
#     plt.ylim((0, 12))
#     plt.axis('equal')
#     plt.tight_layout()
#     plt.savefig('p'+stStr+".png", dpi=300)
#
#
# plot_it()
