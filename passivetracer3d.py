import h5py
import numpy as np
import matplotlib.pyplot as plt

outputDir = "/run/user/1000/gvfs/sftp:host=lisa.surfsara.nl,user=alaik/home/alaik/uw_py3_3D/3dLo/"

# fH = open(outputDir + "/checkpoint.log", "r")
#
# with open(outputDir + "/checkpoint.log", "r") as infile, open(
#     outputDir + "/tRcheckpoint.log", "w+"
# ) as outfile:
#     temp = infile.read().replace(";", "")
#     outfile.write(temp)

time = np.genfromtxt(outputDir + "/tcheckpoint.log", delimiter=",")

for i in time[:, 0]:
    stStr = str(int(i)).zfill(5)
    with h5py.File(outputDir + "tswarm-" + stStr + ".h5", "r") as f:
        tcord = f["data"][()]
    with h5py.File(outputDir + "tcoords-" + stStr + ".h5", "r") as f:
        ic = f["data"][()]

    crX = tcord[:, 0]
    crZ = tcord[:, 2]
    inX = ic[:, 0]
    inZ = ic[:, 2]
    width = 1/8.
    hz = np.zeros_like(inX)
    matC = np.zeros_like(inX)
    matC[:] = 0
    hz[:] = -1
    gX = np.where(np.abs(np.cos(np.pi*5.001*inX)) > .99)
    gZ = np.where(np.abs(np.cos(np.pi*5.001*inZ)) > .99)

    mat = np.where((inZ < 2.0) & (inX > 0.05))
    slabF = np.where((inZ <= 2.0) & (inX <= 2.0) & (inX >= 0.05))
    overF = np.where((inZ <= 2.0) & (inX >= 2.0))
    indeF = np.where((inZ <= 1.0) & (inZ >= 0.2)
                     & (inX <= 0.9) & (inX >= 0.05))
    hz[gX] = 1
    hz[gZ] = 1
    matC[slabF] = 1
    matC[overF] = 2
    matC[indeF] = 3
    hatch = (((np.round(inZ/width) % 2)-(np.round(inX/width) % 2)))
    # plt.plot(hatch)

    def plot_it():
        plt.clf()
        plt.xlim((0, 4))
        plt.ylim((0, 4))
        plt.scatter(crZ[mat], crX[mat], c=matC[mat], s=5, marker='o',cmap="Spectral")
        plt.scatter(crZ[gX], crX[gX], c='black', s=7, marker='.')
        plt.scatter(crZ[gZ], crX[gZ], c='black', s=7, marker='.')
        plt.gcf().set_size_inches(12, 12)
        plt.savefig('gd/pF'+stStr+".png", dpi=120)

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
