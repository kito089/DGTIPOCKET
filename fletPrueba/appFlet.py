from typing import Any, List, Optional, Union
import flet
from flet import *
from functools import partial
import time

from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import AnimationValue, ClipBehavior, OffsetValue, ResponsiveNumber, RotateValue, ScaleValue

class BurgerMenu(UserControl):
    def __init__(self):
        super().__init__()

    def build(self):
        return Container(content=None)
    
def main(page: Page):
    page.title = 'Burger Menu'

    page.horizontal_alignment='left'
    page.vertical_alignment='center'

    page.add(
        Container(
            width=200,
            height=580,
            bgcolor='black',
            content=BurgerMenu()
        )
    )
    page.update()

if __name__ == "__main__":
    flet.app(target=main)