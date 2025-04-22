from typing import (
    Any, AnyStr, Callable, Dict, List, Literal, Optional, Sequence,
    SupportsFloat, SupportsIndex, Tuple, Union, overload,
)


_SupportsFloatorIndex = SupportsIndex | SupportsFloat
from pyms.fm import Angle, DEGREES, RADIANS
_DAGORRAD = Union[DEGREES, RADIANS]
Angle = Angle
DEGREES = DEGREES
RADIANS = RADIANS
import pygame
from pygame import *
from pygame.locals import *
from easygui import *


def system(command: Union[str, bytes, PathLike[str], PathLike[bytes]]) -> int:...

_Num = int | float
_Color = List[int, int, int] | Tuple[int, int, int] | pygame.Color | str | int | List[int, int, int, int]| Tuple[int, int, int, int]
_Pos = List[_Num, _Num] | Tuple[_Num, _Num]
_Size = List[int, int] | Tuple[int, int]
_File = AnyStr
_Image = _Color | pygame.Surface | _File | Tuple[_File] | List[_File]
_AnyCall = Callable[[], Any]
_Call = _AnyCall
_NoneCall = Callable[[], None]
_NoneCommand = lambda: None
_BoolCall = Callable[[], bool]
_SpriteOperation = Surface | Sprite  | int | _Pos
def get_screen(
    size: Coordinate = (0, 0),
    flags: int = 0,
    depth: int = 0,
    display: int = 0,
    vsync: int = 0,
) -> Surface: ...
LEFT: str
RIGHT: str
TOP: str
BOTTOM: str
TOPLEFT: str
BOTTOMRIGHT: str
BOTTOMLEFT: str
TOPRIGHT: str
NONE: str
info: pygame.display.VidInfo
maxWidth: int
maxHeight: int
maxSize: Tuple[int, int]
FRRT: str
FLAR: str
NRTT: str


class Sound:
    @overload
    def __init__(self, file: FileArg) -> None: ...
    
    @overload
    def __init__(
            self, buffer: Any
    ) -> None: ... 
    
    @overload
    def __init__(
            self, array: numpy.ndarray
    ) -> None: ...  
    
    def play(
            self,
            loops: int = 0,
            maxtime: int = 0,
            fade_ms: int = 0,
    ) -> Channel: ...
    __array_interface__: Dict[str, Any]
    __array_struct__: Any
    
    def stop(self) -> None: ...
    
    def fadeout(self, time: int) -> None: ...
    
    def set_volume(self, value: float) -> None: ...
    
    def get_volume(self) -> float: ...
    
    def get_num_channels(self) -> int: ...
    
    def get_length(self) -> float: ...
    
    def get_raw(self) -> bytes: ...
    
class Sprite(pygame.sprite.Sprite):
    old_image: pygame.Surface # If you want to blit surface on image, you must use Sprite.blit or old_image
    image: pygame.Surface
    rect: pygame.Rect
    angle: Angle
    name: str
    x: int
    y: int
    top: int
    left: int
    bottom: int
    right: int
    topleft: _Pos
    bottomleft: _Pos
    topright: _Pos
    bottomright: _Pos
    midtop: _Pos
    midleft: _Pos
    midbottom: _Pos
    midright: _Pos
    center: _Pos
    centerx: int
    centery: int
    size: _Size
    width: int
    height: int
    w: int
    h: int
    
    def __len__(self) -> int:...
    def touchedge(self, sreecn_rect: pygame.Rect, turn_backNone: bool = True) -> str | None:...
    def collidelist(self, rects: Sequence[RectValue]) -> int: ...
    @overload
    def collidepoint(self, x: float, y: float) -> bool: ...
    @overload
    def collidepoint(self, x_y: Coordinate) -> bool: ...
    @overload
    def colliderect(self, rect: RectValue) -> bool: ...
    @overload
    def colliderect(self, left_top: Coordinate, width_height: Coordinate) -> bool: ...
    @overload
    def colliderect(
        self, left: float, top: float, width: float, height: float,
    ) -> bool: ...
    def __add__(self, other: _SpriteOperation) -> Sprite:...
    def __iadd__(self, other: _SpriteOperation) -> None:...
    def __sub__(self, other: _SpriteOperation) -> Sprite:...
    def __isub__(self, other: _SpriteOperation) -> None:...
    def becomeLarger(self, size: int, speed: int  = 1) -> None:...
    def becomeSmaller(self, size: int, speed: int = 1) -> None:...
    @overload
    def set_angle(self, angle: Angle) -> None:...
    @overload
    def set_angle(
        self,
        types: _DAGORRAD,
        number: _SupportsFloatorIndex,
    ) -> None:...
    @overload
    def angleleft(self, angle: Angle) -> None:...
    @overload
    def angleleft(
        self,
        types: _DAGORRAD,
        number: _SupportsFloatorIndex,
    ) -> None:...
    @overload
    def angleright(self, angle: Angle) -> None:...
    @overload
    def angleright(
        self,
        types: _DAGORRAD,
        number: _SupportsFloatorIndex,
    ) -> None:...
    def _alpha(self, alpha: _Color) -> Surface:...
    def alpha(self, alpha: _Color) -> None:...
    def resize(self, size: _Size) -> None:...
    @overload
    def __init__(
            self,
            image: _File | pygame.Surface,
            size: _Size | None = None,
            angle: Angle = Angle(RADIANS, 0),
            filp_mode: str = FRRT,
            *groups: pygame.sprite.Group,
    ) -> None:...
    @overload
    def __init__(
            self,
            image: None = None,
            size: _Size = None, # If it is empty, an error will be reported
            angle: Angle = Angle(RADIANS, 0),
            filp_mode: str = FRRT,
    ) -> None:...
    @overload
    def __init__(
            self,
            image: _Color | None,
            size: _Size,
            angle: Angle = Angle(RADIANS, 0),
            filp_mode: str = FRRT,
            *groups: Group,
    ) -> None:...
    def start_run(self) -> None:...
    def stop_run(self) -> None:...
    def suspend_run(self) -> None:...
    def continue_run(self) -> None:...
    @overload
    def set_image(
            self,
            image: _File | pygame.Surface,
            size: _Size | None = None,
            alpha: _Color | None = ...,
    ) -> None:...
    @overload
    def set_image(
            self,
            image: False,
            size: _Size,
            alpha: _Color | None = ...,
    ) -> None:...
    @overload
    def set_image(
            self,
            image: Sprite,
    ) -> None:...
    @overload
    def set_image(
            self,
            image: _Color | None,
            size: _Size,
            alpha: _Color | None = ...,
    ) -> None:...
    @overload
    def set_image(
        self,
        size: _Size,
        alpha: _Color | None = ...,
    ) -> None:...
    def forward(self, toForward: int) -> None:...
    def backword(self, toBackword: int) -> None:...
    @overload
    def update(self) -> None:...
    @overload
    def update(
        self,
        image: _File | pygame.Surface,
        size: _Size | None = None,
        alpha: _Color | None = ...,
    ) -> None: ...
    @overload
    def update(
        self,
        image: False,
        size: _Size,
        alpha: _Color | None = ...,
    ) -> None: ...
    @overload
    def update(
        self,
        image: Sprite,
    ) -> None: ...
    @overload
    def update(
        self,
        image: _Color | None,
        size: _Size,
        alpha: _Color | None = ...,
    ) -> None: ...
    @overload
    def update(
            self,
            size: _Size,
            alpha: _Color | None = ...,
    ) -> None: ...
    @overload
    def update(self, x: _Num, y: _Num) -> None:...
    @overload
    def update(self, xy: _Pos) -> None:...
    def angle_collide(
            self,
            angle: Literal["top", "bottom", "left", "right"],
            group: Iterable[Sprite],
            kill: bool = False
    ) -> bool:...
    @overload
    def blit(self, sprite: pygame.sprite.Sprite) -> None:...
    @overload
    def blit(self, image: pygame.Surface, rect: pygame.Rect) -> None:...

    topleft = xy = property(lambda self:tuple(), lambda self, value: None, lambda self: None)

def check_mouse(sprite: Rect | Sprite, op: Union[pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, None]) -> bool | pygame.event.Event | None:...

class Button(Sprite):
    image: pygame.Surface
    rect: pygame.Rect
    command: _Call
    text: Text
    
    @overload
    def bind(self, key: int) -> None:...
    @overload
    def bind(self) -> int:...
    
    def __init__(
            self,
            size: _Size,
            text: str,
            command: Callable[[int], Any] | _Call = _NoneCommand,
            color: _Color = ...,
            *groups: Group,
            image: _Image | None = None,
            text_color: _Color = ...,
            font: str | None = None,
    ) -> None:...
    def changeSize(self, stopCommand: _BoolCall, size: int = 10, speed: int = 1) -> None:...
    def touch(self, pos: _Pos | None = None) -> None:...
    def click(
            self,
            pos: _Pos | None = None,
    ) -> bool:...
    def update(
            self,
            text: str | None = None,
            text_color: _Color | None = None,
            color: _Color | None = None
    ) -> None:...


pygame_Sprite = pygame.sprite.Sprite
Group = pygame.sprite.Group
Surface = pygame.Surface
Rect = pygame.Rect
Color = pygame.Color
pygame = pygame


class Background:
    surface: Surface
    background: Optional[Sprite]
    background_groups: list
    __groups: list

    def groups(self) -> tuple:...
    def draw(self) -> None:...
    def backgrounds(self) -> tuple:...
    def __init__(
            self,
            surface: Optional[Surface],
            background: Surface | None | _Color = None,
            *sprites: Sprite,
    ) -> None:...
    def add_group(self, group: Group) -> None:...
    def remove_group(self, group: Group) -> None:...
    def has_group(self, group: Group) -> bool:...
    def add_backgrounds(self, backgrounds: Backgrounds) -> None:...
    def remove_backgrounds(self, backgrounds: Backgrounds) -> None:...
    def has_backgrounds(self, backgrounds: Backgrounds) -> bool:...
    def add(self, *backgroundses: Background | Group | Iterable[Background | Group, ...]) -> None:...
    def remove(self, *backgroundses: Background | Group | Iterable[Background | Group, ...]) -> None:...
    def update(self, *args: Any, **kw: Any) -> None:...
    def __repr__(self) -> str:...
    def __iter__(self) -> Iterable:...
    def __len__(self) -> int:...
    def copy(self) -> Background:...
    __copy__ = copy


default_background: Background | None = None

def setDefaultbackground(background: Background) -> None:...
class Backgrounds:
    backgrounds: list
    default_background: Background | None
    mode: Surface
    def copy(self) -> Backgrounds:...
    def __copy__(self) -> Backgrounds:...

    def set_background(self, backdround: Background) -> None:...
    def draw(self, surface: Surface | None = None, find: bool = ...) -> None:...
    def add_background(self, background: Background) -> None:...
    def remove_background(self, background: Background) -> None:...
    def has_background(self, background: Background) -> bool:...
    def add(self, *backgrounds) -> None:...
    def remove(self, *backgrounds) -> None:...
    def __repr__(self) -> str: ...
    def __iter__(self) -> Iterable: ...
    def __len__(self) -> int: ...
    def __init__(self, *backgrounds: Background) -> None:...


class Text(pygame.sprite.Sprite):
    font: pygame.font.Font
    color: Color
    image: pygame.Surface
    rect: pygame.Rect
    text: str
    def set_text(self, text: str) -> None:...
    def __init__(
            self,
            font_size: int,
            text: str = "",
            color: _Color = ...,
            font: str | None | Any = None,
            *groups: Group,
    ) -> None:...
    @overload
    def update(self, text: str | None = None, color: _Color | None = None) -> None:...
    @overload
    def update(self, text: str, color: _Color, x: _Num, y: _Num) -> None:...
    @overload
    def update(self, *, x: _Num, y: _Num) -> None:...
    @overload
    def update(self, *, x: _Pos) -> None:...
    @overload
    def update(self, text: str, color: _Color, xy: _Pos) -> None: ...


class RoundedRect(Sprite):
    fillcolor: _Color
    round_size: _Size
    side_width: int
    sidecolor: _Color
    @overload
    def __init__(
            self,
            color: _Color,
            round_rect: _Size,
            rect: _Size,
            *,
            width: int,
            side_color: _Color,
    ) -> None: ...
    @overload
    def __init__(
            self,
            color: _Color,
            round_rect: _Size,
            all_width: int,
            all_height: int,
            *,
            width: int,
            side_color: _Color,
    ) -> None: ...
    @overload
    def __init__(
            self,
            color: _Color,
            round_rect: _Size,
            rect: _Size,
    ) -> None: ...
    @overload
    def __init__(
            self,
            color: _Color,
            round_rect: _Size,
            all_width: int,
            all_height: int,
    ) -> None: ...
    @overload
    def update(
            self,
            color: _Color,
            round_rect: _Size,
            rect: _Size,
            *,
            width: int,
            side_color: _Color,
    ) -> None: ...
    @overload
    def update(self) -> _Pos:...
    @overload
    def update(
            self,
            color: _Color,
            round_rect: _Size,
            rect: _Size,
    ) -> None: ...
    @overload
    def update(
            self,
            color: _Color,
            round_rect: _Size,
            all_width: int,
            all_height: int,
    ) -> None: ...
    @overload
    def update(
            self,
            color: _Color,
            round_rect: _Size,
            all_width: int,
            all_height: int,
            *,
            width: int,
            side_color: _Color,
    ) -> None: ...
    @overload
    def draw(
            self,
            color: _Color,
            round_rect: _Size,
            rect: _Size,
    ) -> None:...
    @overload
    def draw(
            self,
            color: _Color,
            round_rect: _Size,
            all_width: int,
            all_height: int,
    ) -> None:...
    @overload
    def draw(
            self,
            color: _Color,
            round_rect: _Size,
            all_width: int,
            all_height: int,
            *,
            width: int,
            side_color: _Color,
    ) -> None: ...
    @overload
    def draw(
            self,
            color: _Color,
            round_rect: _Size,
            rect: _Size,
            *,
            width: int,
            side_color: _Color,
    ) -> None: ...

class RoundButton(RoundedRect, Button):
    @overload
    def __init__(
            self,
            size: _Size,
            round_size: _Size,
            text: str,
            fillcolor: _Color,
            command: _Call = _NoneCommand,
            *groups: Group,
            textcolor: _Color = ...,
    ) -> None:...
    @overload
    def __init__(
            self,
            size: _Size,
            round_size: _Size,
            text: str,
            fillcolor: _Color,
            command: _Call = _NoneCommand,
            *groups: Group,
            width: int,
            sidecolor: _Color,
            textcolor: _Color = ...,
    ) -> None:...
    def update(
            self,
            text: str | None = None,
            text_color: _Color | None = None,
            color: _Color | None = None
    ) -> None:...


class RoundEdgeButton(RoundButton):
    @overload
    def __init__(
            self,
            size: _Size,
            length: _Num,
            text: str,
            fillcolor: _Color,
            command: _Call = _NoneCommand,
            *groups: Group,
            textcolor: _Color = ...,
    ) -> None: ...
    
    @overload
    def __init__(
            self,
            size: _Size,
            length: _Num,
            text: str,
            fillcolor: _Color,
            command: _Call = _NoneCommand,
            *groups: Group,
            width: int,
            sidecolor: _Color,
            textcolor: _Color = ...,
    ) -> None: ...


class Circle(Sprite):
    def __init__(
            self,
            diameter: float,
            color: _Color,
            width: int = 0,
            draw_top_right: bool = False,
            draw_top_left: bool = False,
            draw_bottom_left: bool = False,
            draw_bottom_right: bool = False,
    ) -> None:...


class CircleButton(RoundButton):
    @overload
    def __init__(
            self,
            diameter: float,
            text: str,
            fillcolor: _Color,
            command: _Call = _NoneCommand,
            *groups: Group,
            textcolor: _Color = ...,
    ) -> None: ...
    
    @overload
    def __init__(
            self,
            size: _Size,
            text: str,
            fillcolor: _Color,
            command: _Call = _NoneCommand,
            *groups: Group,
            width: int,
            sidecolor: _Color,
            textcolor: _Color = ...,
    ) -> None: ...

class Barrage(Sprite):
    text: Text
    _pixel: pygame.PixelArray
    width: int
    height: int
    speed: int
    yspeed: int
    def __init__(
            self,
            text: str,
            size: _Size = ...,
            color: _Color = ...,
            text_color: _Color = ...,
            speed: int = 1,
            yspeed: int = 10,
    ) -> None:...
    def update(self, speed: int | None = None) -> None:...

def toKeyboardInterrrupt(command: _Call = _NoneCommand) -> None:...
def terminate(code: Any = 0, command: _Call = _NoneCommand) -> None:...
def toTerminate(code: Any = 0, command: _Call = _NoneCommand) -> _Call:...
def CheckForQuit(minmize: int | None | False = ..., savecommand: _Call = _NoneCommand) -> None:...
def CheckForMinmize(key: int = ...) -> None:...
def CheckForResize() -> _Size:...
def toList(surf: Surface) -> List[Tuple[int, int, int, int]]:...

colors: Dict[str, Tuple[int, int, int, 255]]
Clock = pygame.time.Clock
clock: Clock

def tick(fps: float = 0) -> float:...
def toColor(color: _Color, raised: bool = True) -> Color:...
def blend_rgba(color1: Color, color2: Color):...

WHITE: Color
BLACK: Color
RED: Color
BLUE: Color
GREEN: Color
ORANGE: Color
