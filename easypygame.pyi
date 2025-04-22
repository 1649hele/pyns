from typing import (
    Any, Callable, Sequence, SupportsFloat, List, Tuple,
    AnyStr, SupportsIndex, overload, Optional
)
import flat_gui_base as _base
from Windows.pyms.flat_gui_base import Angle


def fixed_parameters(func: Callable[[Any], Any], *args: Any, **kwargs: Any) -> Callable[[], Any]:...
_Num = int | float
_Pos = List[_Num, _Num] | Tuple[_Num, _Num]
_Color = (
    List[int, int, int] |
    Tuple[int, int, int] |
    _base.Color |
    AnyStr |
    int |
    List[int, int, int, int] |
    Tuple[int, int, int, int]
)
_File = AnyStr
_Image = _Color | _base.Surface | _File | Tuple[_File] | List[_File]
from pyms.fm import Angle, DEGREES, RADIANS
DEGREES = DEGREES
RADIANS = RADIANS
_DAGORRAD = Union[DEGREES, RADIANS]

def rotate_point(a0: _Pos, a1: _Pos, angle: SupportsFloat) -> _Pos:...
FPS: _Num

class Sprite(_base.Sprite):
    shapes: List[_Image]
    shape_index: SupportsIndex
    shape_size: SupportsFloat
    relative_center: _Pos
    def __init__(self, shapes: List[_Image]) -> None:...
    def update(self, *args: Any, **kwargs: Any) -> None:...
    def set_shape(self, index: SupportsIndex) -> None:...
    def next_shape(self) -> None:...

    def angleright(
        self,
        (
            types: _DAGORRAD,
            number: _Num,
        ),
        center: Optional[_Pos] = None,
    ) -> None:...
    def angleleft(
        self,
        (
            types: _DAGORRAD,
            number: _Num
        ),
        center: Optional[_Pos] = None
    ) -> None:...
    def goto(self, x: _Num, y: _Num) -> None:...

def delay(time: SupportsFloat) -> None:...
def complete_within(func: Callable[[],type(None)], time: SupportsFloat) -> None:...

_broadcasts: Set[AnyStr]

def make_broadcast(name: AnyStr) -> None: ...
def receive_broadcast(name: AnyStr) -> bool: ...
def get_ticks() -> int: ...
def get_distance(a0: Tuple[float, float], a1: Tuple[float, float]) -> float: ...

def click(
    keys: Tuple[int, ...] = (1,),
    max_time: int = 500,
    max_distance: int = 5,
    rect: Optional[_pygame.Rect] = None
) -> bool: ...

def press_key(keys: Tuple[int, ...], types: int) -> Optional[_base.event.Event]: ...
@overload
def mouse_position(x: Optional[Tuple[int, int]]) -> None:...
@overload
def mouse_position() -> Tuple[int, int]: ...
def check_event(types: int) -> Optional[_pygame.event.Event]: ...
def check_basic() -> Optional[_pygame.event.Event]: ...

def start(
    func: Callable[..., Any],
    start_factor: Callable[..., bool],
    times: Optional[int] = None,
    new_thread: bool = True
) -> None: ...

def update() -> None: ...
def start_game() -> None: ...
def quit() -> None: ...
@overload
def screen_size(size: Tuple[int, int]) -> None:...
@overload
def screen_size() -> Tuple[int, int]: ...
