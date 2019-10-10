import underworld as uw
from collections import OrderedDict
from checkpoint import checkpoint
from scaling import dm, nd, u
import underworld.visualisation as viz

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
swarmDict["svar"] = svar

if restartFlag is False:
    checkpoint(mesh, fieldDict, swarm, swarmDict,
               index=0, prefix="outputTest2/")

if restartFlag is True:
    checkpoint(mesh, fieldDict, swarm, swarmDict,
               index=0, prefix="outputTest2/", load=True)

nd(9.8 * u.metre / u.second ** 2*80*u.kilogram / u.meter ** 3)
dm(1.0, u.pascal*u.second)

figM = viz.Figure()
figM.Mesh(mesh)
figM.Points(swarm, svar, pointSize=10)
figM.show()
