 
import numpy as np
from typing import Callable

from ..arithmetic import linalg
from ..structures import Lattice
from ..stats import constant
from .Model import Model


class SwendsenWang(Model):
    name = "SwendsenWang"
    
    def __init__(
            self, L: Lattice, temperatureFunction: Callable=constant(-0.6),
            initial=None
        ):
        """
        Initializes Swendsen-Wang evolution on the Potts model.

        Args:
            L: The `Lattice` object on which we'll be running experiments.
            temperatureFunction (Callable): A temperature schedule function which
                takes a single positive integer argument `t`, and returns the
                scheduled temperature at time `t`.
            initial (np.ndarray): A vector of spin assignments to components.
        """
        self.lattice = L
        self.temperatureFunction = temperatureFunction

        # SW defaults.
        self.state = initial if initial else self.initial()
        self.spins = { face: self.state[self.lattice.index.faces[face]] for face in self.lattice.faces }
        self.occupied = set()


    def initial(self) -> np.array:
        """
        Computes an initial state for the model's Lattice.

        Returns:
            A NumPy array representing a vector of spin assignments.
        """
        return np.array([np.random.randint(0, self.lattice.field.order) for _ in self.lattice.faces])
    

    def proposal(self, time):
        """
        Proposal scheme for generalized Swendsen-Wang evolution on the Potts model.

        Args:
            time (int): Step in the chain.

        Returns:
            A NumPy array representing a vector of spin assignments.
        """
        # Compute the probability of choosing any individual cube in the complex.
        self.temperature = self.temperatureFunction(time)
        p = 1-np.exp(self.temperature)
        assert 0 <= p <= 1

        # Choose cubes (i.e. columns) to include: we do so by asking whether the
        # sum o f the faces is 0 and a weighted coin flip succeeds.
        includeCubes = []
        
        for cube in self.lattice.cubes:
            q = np.random.uniform()
            null = self.lattice.field([self.spins[face] for face in cube.faces]).sum() == 0

            if null and q < p:
                includeCubes.append(cube)

        includeCubeIndices = [self.lattice.index.cubes[cube] for cube in includeCubes]
        self.occupied = set(includeCubes)

        # Uniformly randomly sample a cocycle on the sublattice admitted by the
        # chosen edges; reconstruct the labeling on the entire lattice by
        # subbing in the values of c which differ from existing ones.
        return linalg.sampleFromKernel(self.lattice.coboundary, self.lattice.field, includeCubeIndices)
    

    def assign(self, cocycle: np.array):
        """
        Updates mappings from faces to spins and cubes to occupations.

        Args: 
            cocycle (np.array): Cocycle on the sublattice.
        """
        self.spins = { face: cocycle[self.lattice.index.faces[face]] for face in self.lattice.faces }
        
        # Dual graph of sublattice of occupied cubes.
        # self.lattice.subgraph = self.lattice.graph.subgraph(
        #     [self.lattice.index.cubes[cube] for cube in self.lattice.cubes if not cube in self.occupied]
        # )