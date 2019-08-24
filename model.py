import underworld as uw
from collections import OrderedDict
from checkpoint import checkpoint

mesh = uw.mesh.FeMesh_Cartesian()
mvar = mesh.add_variable(nodeDofCount=mesh.dim)

fieldDict = OrderedDict()  # important to avoid racing conditions
fieldDict["mvar"] = mvar

swarm = uw.swarm.Swarm(mesh=mesh)
svar = swarm.add_variable('int', 1)

swarmDict = OrderedDict()  # important to avoid racing conditions
swarmDict["svar"] = svar

checkpoint(mesh, fieldDict, swarm, swarmDict,
           index=0, prefix="outputTest/")

checkpoint(mesh, fieldDict, swarm, swarmDict,
           index=0, prefix="outputTest", load=True)
