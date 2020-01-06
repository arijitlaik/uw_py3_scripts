import underworld as uw
import underworld.function as fn
from collections import OrderedDict
from checkpoint import checkpoint
from scaling import dm, nd, u
import underworld.visualisation as viz
import numpy as np
import os
# restartFlag = False
restartFlag = True
mesh = uw.mesh.FeMesh_Cartesian()
mvar = mesh.add_variable(nodeDofCount=mesh.dim)

fieldDict = OrderedDict()  # important to avoid racing conditions
fieldDict["mvar"] = mvar

swarm = uw.swarm.Swarm(mesh=mesh)
svar = swarm.add_variable('int', 1)

swarmLayout = uw.swarm.layouts.PerCellSpaceFillerLayout(
    swarm=swarm, particlesPerCell=20
)
if restartFlag is False:
    swarm.populate_using_layout(layout=swarmLayout)


swarmDict = OrderedDict()  # important to avoid racing conditions
swarmDict["tcoords"] = svar
svar.data[:] = 0
svar.data[fn.coord()[0].evaluate(swarm) > 0.5] = 1
outputDirName = "t3d_960_llr"


outputDir = os.path.join(os.path.abspath("."), outputDirName + "/")
if restartFlag is False:
    checkpoint(mesh, fieldDict, swarm, swarmDict,
               index=0, prefix=outputDir)

if restartFlag is True:
    checkpoint(mesh, fieldDict, swarm, swarmDict,
               index=0, prefix=outputDir, load=True)

nd(9.8 * u.metre / u.second ** 2*80*u.kilogram / u.meter ** 3)
dm(1.0, u.pascal*u.second)

figM = viz.Figure(rulers=True, figsize=(450, 500))
figM.Mesh(mesh)
figM.Points(swarm, svar, pointSize=10)
figM.show()

svarIsOne = np.where(svar.data[:] == 1)[0]
swarm.data[svarIsOne]
