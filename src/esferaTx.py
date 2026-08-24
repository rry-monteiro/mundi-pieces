from ursina import Entity, application, curve, Vec3, Func
from pathlib import Path
from panda3d.core import Filename

"""
{{{ESSSA ESFERA TEM A TEXTURA DA TERRA}}}


A classe ESFERA é herdeira de Entity
(isso faz a esfera ser vista como UMA entidade, posso mover a vontade)

modo de uso:
esfera = Esfera(colors_list=[LISTA DE CORES >8<], shader=algumshader)

assim as cores se distribuem pelas partes e o shader é aplicado em todas
"""


class Esfera(Entity):
    def __init__(
        self,
        explode_positons: list,  # lista de posições pra explode
        mouse_on_positions: list,  # lista de posições pra mouse=on
        mouse_click_positions: list,  # lista de posições pra click
        shader: object,  # shader para luz
        diret: str,  # pasta dos modelos
    ):
        super().__init__()  # puxa tudo de Entity

        self.explode_positons = explode_positons
        self.mouse_on_positions = mouse_on_positions
        self.mouse_click_positions = mouse_click_positions

        diret_path = Path(diret)
        self.models = sorted([p.name for p in diret_path.glob("*.glb")])

        loader = application.base.loader

        self.partes = [
            Entity(
                # cores removidas devido ao uso de textura
                # rotação no eixo x e z removidas devido ao modelo glb
                # a rotação teve que voltar pq o EXE quebrou o código kkk
                # rotation=Vec3(0, -90, 0),
                model=loader.loadModel(
                    Filename.fromOsSpecific(str((diret_path / model).resolve()))
                ),
                # alterando a escala em x pq o EXE ta quebrando o codigo dnv
                scale=(-1, 1, 1),
                # a rotação teve que MUDAR pq o scale_x quebrou DNV O CODIGO
                rotation=Vec3(0, 180, 0),
                shader=shader,
                collider="mesh",
                # daqui pra baixo são as funções aplicadas a ESFERA
                on_mouse_enter=Func(self.on_emphasis_part, n, mouse_on_positions[n]),
                on_mouse_exit=Func(
                    self.off_emphasis_part,
                    n,
                ),
                on_click=Func(self.move_part, n, mouse_click_positions[n]),
                at_the_origin=True,
            )
            for n, model in enumerate(self.models)
        ]

    """MOVE UMA PARTE DA ESFERA"""
    """
    se a parte estiver na origem, ela move de acordo com as
    posições definidas (self.mouse_click_positions[n])

    senão, significa que a parte ja foi clicada com a esfera
    foi explodida, volta a parte pra origem (Vec3(0,0,0))
    """

    def move_part(self, index_part: int, position: tuple):

        # definindo a parte que eu vou usar
        part = self.partes[index_part]

        if part.at_the_origin == True:
            part.at_the_origin = False
            part.animate_position(
                value=position, duration=0.5, interrupt="finish", curve=curve.out_sine
            )
        else:
            part.at_the_origin = True
            part.animate_position(
                value=Vec3(0, 0, 0),
                duration=0.5,
                interrupt="finish",
                curve=curve.out_sine,
            )
        return

    """DESTACA A PARTE AO PASSAR O MOUSE"""

    def on_emphasis_part(self, index_part: int, position: tuple):

        # definindo a parte que eu vou usar
        part = self.partes[index_part]

        if part.at_the_origin == True:
            part.animate_position(
                value=position, duration=0.1, interrupt="kill", curve=curve.out_sine
            )
        return

    """REMOVE O DESTAQUE DADO A PARTE AO PASSAR O MOUSE"""

    def off_emphasis_part(self, index_part: int):

        # definindo a parte que eu vou usar
        part = self.partes[index_part]

        if part.at_the_origin == True:
            part.animate_position(
                value=Vec3(0, 0, 0),
                duration=0.1,
                interrupt="kill",
                curve=curve.out_sine,
            )
        return

    """EXPLODE A ESFERA"""

    def explode_sphere(self):
        for part, position in zip(self.partes, self.explode_positons):
            part.at_the_origin = False
            part.animate_position(
                value=position, duration=0.5, interrupt="finish", curve=curve.out_sine
            )
        return

    """IMPLODE A ESFERA"""

    def implode_sphere(self):
        for part in self.partes:
            part.at_the_origin = True
            part.animate_position(
                Vec3(0, 0, 0), duration=0.5, interrupt="finish", curve=curve.out_sine
            )
        return
