
from ..arithmetic import flattenAndSortSetUnion, elementwiseAddOne

class ReducedCell:
    """
    Cells for the lattice, but encoded using NumPy for performance advantages;
    carries far less data.
    """
    def __init__(self, encoding, faces=None):
        self.encoding = self._sortEncoding(encoding)
        self.faces = set(faces) if faces else None
        self.hash = hash(self.encoding)
        self.str = str(self.encoding)
        self.index = None
    
    @staticmethod
    def _sortEncoding(encoding): return tuple(sorted(tuple(encoding)))

    # Comparisons.
    def __lt__(self, other): return self.encoding < other.encoding
    def __gt__(self, other): return self.encoding > other.encoding
    def __eq__(self, other): return self.encoding == other.encoding

    # Things for hashes and stringifications; we compute them once, and return
    # them always.
    def __str__(self): return self.str
    def __hash__(self): return self.hash


class Cell:
    def __init__(self, faces, vertex=False):
        self.dimension = 0 if vertex else faces[0].dimension+1
        self.vertices = [faces] if vertex else flattenAndSortSetUnion([face.vertices for face in faces])
        self.encoding = tuple(self.vertices) + (self.dimension,)
        self.faces = set() if self.dimension == 0 else set(faces)

        self.hash = hash(self.encoding)
        self.str = str(self.encoding)
        

    def reEncode(self):
        """
        If changes are made to this Cell, we re-compute its encoding and vertices.
        """
        self.vertices = self.vertices if self.dimension==0 else flattenAndSortSetUnion([face.vertices for face in self.faces])
        self.encoding = tuple(self.vertices) + (self.dimension,)

        self.hash = hash(self.encoding)
        self.str = str(self.encoding)


    def __lt__(self, other): return self.encoding < other.encoding
    def __gt__(self, other): return self.encoding > other.encoding
    def __eq__(self, other): return self.encoding == other.encoding

    def __str__(self): return self.str
    def __hash__(self): return self.hash




class IntegerCell:
    def __init__(self, faces, vertex=False):
        self.dimension = 0 if vertex else faces[0].dimension+1
        self.vertices = [faces] if vertex else flattenAndSortSetUnion([face.vertices for face in faces])
        self.encoding = tuple(self.vertices) + (self.dimension,)
        self.faces = set(faces if self.dimension > 0 else [faces])

        self.hash = hash(self.encoding)
        self.str = str(self.encoding)

    def shiftedEncoding(self, k):
        return tuple(elementwiseAddOne(self.vertices, k)) + (self.dimension,)
    
    def __lt__(self, other): return self.encoding < other.encoding
    def __gt__(self, other): return self.encoding > other.encoding
    def __eq__(self, other): return self.encoding == other.encoding

    def __str__(self): return self.str
    def __hash__(self): return self.hash


class Vertex:
    # TODO consolidate the GraphLattice and Lattice classes!
    pass
