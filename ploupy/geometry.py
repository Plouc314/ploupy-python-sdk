from typing import Iterable
import numpy as np
from scipy.cluster.vq import kmeans2

from .game import Tile
from .models.core import Pos


def distance(a: Pos, b: Pos) -> float:
    """
    Return the distance between the two positions
    """
    return np.sqrt(((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2))


def closest_tile(tiles: Iterable[Tile], pos: Pos) -> Tile | None:
    """
    Return the tile closest to the given position

    Note: return None if `tiles` is empty
    """
    tiles = list(tiles)  # cast iterable
    coords = np.array([tile.coord - pos for tile in tiles])
    if coords.size == 0:
        return None

    dists = np.linalg.norm(coords, axis=1)
    idx = np.argmin(dists)

    return tiles[idx]


def furthest_tile(tiles: Iterable[Tile], pos: Pos) -> Tile | None:
    """
    Return the tile furthest to the given position

    Note: return None if `tiles` is empty
    """
    tiles = list(tiles)  # cast iterable
    coords = np.array([tile.coord - pos for tile in tiles])
    if coords.size == 0:
        return None

    dists = np.linalg.norm(coords, axis=1)
    idx = np.argmax(dists)

    return tiles[idx]


def center(positions: Iterable[Pos]) -> np.ndarray | None:
    """
    Return the center of the positions (as defined by the k-means algorithm)

    Note: return None if `positions` is empty
    """
    _centers = centers(positions, 1)

    if _centers is None:
        return None
    return _centers[0]


def centers(positions: Iterable[Pos], n_center) -> list[np.ndarray]:
    """
    Return the n centers that fit the best for the given positions
    (as defined by the k-means algorithm)
    """
    positions = np.array(list(positions), dtype=float)
    if positions.size == 0:
        return None

    _centers, _ = kmeans2(positions, k=n_center, minit="points")

    return list(_centers)
