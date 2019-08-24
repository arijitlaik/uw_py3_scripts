#!/usr/bin/env python
# coding: utf-8


import os
import sys

import underworld as uw


def print_on_rank_zero(message, *args):
    if uw.mpi.rank == 0:
        print(message, *args)
        sys.stdout.flush()


def create_prefix(prefix):
    # Check the prefix is valid
    if prefix is not None:
        if not prefix.endswith("/"):
            prefix += "/"  # add a backslash
        if not os.path.exists(prefix) and uw.mpi.rank == 0:
            print("Creating directory: ", prefix)
            os.makedirs(prefix)
    return prefix


def check_mesh_and_mvar_type(mesh, fieldDict):
    # Error check the mesh and fields
    if not isinstance(mesh, uw.mesh.FeMesh):
        raise TypeError("'mesh' is not of type uw.mesh.FeMesh")
    if fieldDict is not None:
        if not isinstance(fieldDict, dict):
            raise TypeError("'fieldDict' is not of type dict")
        for key, value in fieldDict.items():
            if not isinstance(value, uw.mesh.MeshVariable):
                raise TypeError(
                    "'fieldDict' must contain uw.mesh.MeshVariable elements"
                )


def check_swarm_and_svar_type(swarm, swarmDict):
    if not isinstance(swarm, uw.swarm.Swarm):
        raise TypeError("'swarm' is not of type uw.swarm.Swarm")
    if swarmDict is not None:
        if not isinstance(swarmDict, dict):
            raise TypeError("'swarmDict' is not of type dict")
        for key, value in swarmDict.items():
            if not isinstance(value, uw.swarm.SwarmVariable):
                raise TypeError(
                    "'SwarmDict' must contain uw.swarm.SwarmVariable elements"
                )


def checkpoint(
    mesh,
    fieldDict,
    swarm,
    swarmDict,
    index,
    modeltime=None,
    meshName="mesh",
    swarmName="swarm",
    prefix="./",
    enable_xdmf=True,
    load=False,
):
    prefix = create_prefix(prefix)

    if not isinstance(index, int):
        raise TypeError("'index' is not of type int")
    if modeltime is not None:
        time = modeltime
    else:
        time = index

    ii = str(index).zfill(5)

    if mesh is not None:

        # Error check the mesh and fields
        check_mesh_and_mvar_type(mesh, fieldDict)

        # see if we have already saved the mesh. It only needs to be saved once
        if not hasattr(checkpoint, "mH"):
            if load:
                print_on_rank_zero("Loading Mesh.....")
                mesh.load(prefix + meshName + ".h5")

            print_on_rank_zero("Saving Mesh.....")
            checkpoint.mH = mesh.save(prefix + meshName + ".h5")
        mh = checkpoint.mH

        for key, value in fieldDict.items():
            filename = prefix + key + "-" + ii
            if load:
                print_on_rank_zero("Loading MeshVariable(s).....")
                print_on_rank_zero("Loading '{0}.h5' .....".format(filename))
                value.load(filename + ".h5")
            else:
                handle = value.save(filename + ".h5")
                if enable_xdmf:
                    value.xdmf(filename, handle, key, mh, meshName, modeltime=time)

    # is there a swarm
    if swarm is not None:

        # Error check the swarms
        check_swarm_and_svar_type(swarm, swarmDict)

        if load:
            print_on_rank_zero("Loading Swarm.....")
            swarm.load(prefix + swarmName + "-" + ii + ".h5")
        else:
            print_on_rank_zero("Saving Swarm.....")
            sH = swarm.save(prefix + swarmName + "-" + ii + ".h5")
        for key, value in swarmDict.items():
            filename = prefix + key + "-" + ii
            if load:
                print_on_rank_zero("Loading SwarmVariable(s).....")
                print_on_rank_zero("Loading '{0}.h5' .....".format(filename))
                value.load(filename + ".h5")
            else:
                handle = value.save(filename + ".h5")
                if enable_xdmf:
                    value.xdmf(filename, handle, key, sH, swarmName, modeltime=time)
    print_on_rank_zero("Done.....")
