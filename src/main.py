from ursina import Ursina, Entity, EditorCamera, Vec3, Button, color, Func, Vec2, camera
import math as mt
import webbrowser
from ursina.models.procedural.grid import Grid
from ursina.shaders import lit_with_shadows_shader
from esferaTx import Esfera

from pathlib import Path

BASE = Path(__file__).resolve().parent

"""
as coordenadas aqui são vistas como:
    x, z, y
o padrão (PyVista, por exemplo) seria:
    x, y, z
"""


"""FAZ OS CALCULOS COM PHI E THETA E RETORNA A TUPLA (X,Z,Y)"""


def cvetor(theta: None, phi: None, r: int):
    """
    x : r * sen(theta) * cos(phi)
    z : r * cos(theta)
    y : r * sen(theta) * sen(phi)
    """
    X = r * mt.sin(theta) * mt.cos(phi)
    Z = r * mt.cos(theta)
    Y = r * mt.sin(theta) * mt.sin(phi)
    return X, Z, Y


"""ABRE O HTML DE AJUDA {python -> html -> ajuda.html}"""


def open_info():
    help_file = BASE / "html" / "info.html"
    webbrowser.open(help_file.resolve().as_uri())


# definindo todas as preferencias do app
APP = Ursina("MUNDI PIECES")

GRIDE = Entity(model=Grid(150, 150), scale=6000, rotation=Vec3(90, 0, 0))

CAMERA = EditorCamera(
    rotation_speed=300,
    rotation_smoothing=10,
)

COLORS_LIST = [
    color.blue,  # 0
    color.magenta,  # 1
    color.gray,  # 2
    color.yellow,  # 3
    color.brown,  # 4
    color.red,  # 5
    color.black,
]  # 6

EXPLODE_POSITONS = [
    cvetor(mt.pi, 0, r=10),
    cvetor(3131 * mt.pi / 7200, 5 * mt.pi / 4, r=10),
    cvetor(3131 * mt.pi / 720, 5 * mt.pi / 4, r=10),
    cvetor(469 * mt.pi / 7200, 5 * mt.pi / 4, r=10),
    cvetor(3131 * mt.pi / 7200, mt.pi / 4, r=10),
    cvetor(mt.pi / 4, mt.pi / 4, r=10),
    cvetor(469 * mt.pi / 7200, mt.pi / 4, r=10),
]

MOUSE_ON_POSITIONS = [
    cvetor(mt.pi, 0, r=0.2),
    cvetor(3131 * mt.pi / 7200, 5 * mt.pi / 4, r=0.2),
    cvetor(3131 * mt.pi / 720, 5 * mt.pi / 4, r=0.2),
    cvetor(469 * mt.pi / 7200, 5 * mt.pi / 4, r=0.2),
    cvetor(3131 * mt.pi / 7200, mt.pi / 4, r=0.2),
    cvetor(mt.pi / 4, mt.pi / 4, r=0.2),
    cvetor(469 * mt.pi / 7200, mt.pi / 4, r=0.2),
]

MOUSE_CLICK_POSITIONS = [
    cvetor(mt.pi, 0, r=5),
    cvetor(3131 * mt.pi / 7200, 5 * mt.pi / 4, r=5),
    cvetor(3131 * mt.pi / 720, 5 * mt.pi / 4, r=5),
    cvetor(469 * mt.pi / 7200, 5 * mt.pi / 4, r=5),
    cvetor(3131 * mt.pi / 7200, mt.pi / 4, r=5),
    cvetor(mt.pi / 4, mt.pi / 4, r=5),
    cvetor(469 * mt.pi / 7200, mt.pi / 4, r=5),
]

mundi = Esfera(
    EXPLODE_POSITONS,
    MOUSE_ON_POSITIONS,
    MOUSE_CLICK_POSITIONS,
    lit_with_shadows_shader,
    str(BASE / "models-tx"),
)

explode = Button(
    "EXPLODE",
    color=color.black,
    origin=(7, 0),
    on_click=mundi.explode_sphere,
    scale=Vec2(0.113, 0.06),
)

implode = Button(
    "IMPLODE",
    color=color.black,
    origin=(7, 2),
    on_click=Func(mundi.implode_sphere),
    scale=Vec2(0.113, 0.06),
)

ajuda = Button(
    "AJUDA",
    parent=camera.ui,
    scale=(0.12, 0.06),
    position=(0.75, 0.45),
    on_click=Func(open_info),
)


APP.run()
