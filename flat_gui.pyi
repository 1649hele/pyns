from typing import (
    Any, AnyStr, Callable, Dict, List, Literal, Optional, Sequence,
    SupportsFloat, SupportsIndex, Tuple, Union, overload,
)


_SupportsFloatorIndex = SupportsIndex | SupportsFloat
from pyns.fm import Angle, DEGREES, RADIANS
_DAGORRAD = Union[DEGREES, RADIANS]
Angle = Angle
import pygame
from pygame import *
from pygame.locals import *


def system(command: Union[str, bytes, PathLike[str], PathLike[bytes]]) -> int:...

_Num = int | float
_Color = List[int, int, int] | Tuple[int, int, int] | pygame.Color | str | int | List[int, int, int, int]| Tuple[int, int, int, int]
_Pos = List[_Num, _Num] | Tuple[_Num, _Num] | pygame.Rect
_Size = List[int, int] | Tuple[int, int]
_File = AnyStr
_Image = _Color | pygame.Surface | _File | Tuple[_File] | List[_File]
_AnyCall = Callable[[], Any]
_Call = _AnyCall
_NoneCall = Callable[[], None]
_NoneCommand = lambda: None
_BoolCall = Callable[[], bool]
_SpriteOperation = Surface | Sprite  | int | _Pos
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
    image: pygame.Surface
    rect: pygame.Rect
    angle: Angle
    name: int
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
            angle: int = 0,
            *groups: pygame.sprite.Group,
    ) -> None:...
    @overload
    def __init__(
            self,
            image: None = None,
            *,
            size: _Size,
            angle: int  = 0,
    ) -> None:...
    @overload
    def __init__(
            self,
            image: _Color | None,
            size: _Size,
            angle: int = 0,
            *groups: Group,
    ) -> None:...
    @overload
    def __init__(
            self,
            size: _Size,
            alpha: _Color | None = ...,
    ) -> None: ...
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
    def update(self) -> _Pos:...
    @overload
    def update(
            self,
            image: Surface | _File,
    ) -> None:...
    @overload
    def update(self, x: _Num, y: _Num) -> None:...
    @overload
    def update(self, xy: _Pos) -> None:...
    @overload
    def update(self, *args: Any, **kwargs: Any) -> None:...
    def angle_collide(
            self,
            angle: Literal["top", "bottom", "left", "right"],
            group: Iterable[Sprite],
            kill: bool = False
    ) -> bool:...

    topleft = xy = property(lambda self:tuple(), lambda self, value: None, lambda self: None)


class Button(Sprite):
    image: pygame.Surface
    rect: pygame.Rect
    command: _Call
    text: Text
    _key: int
    
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
    background: Group | None
    spritebackground: Sprite | None
    background_groups: list
    __groups: list

    def groups(self) -> tuple:...
    def draw(self) -> None:...
    def backgrounds(self) -> tuple:...
    def __init__(
            self,
            surface: Surface,
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
    def __copy__(self) -> Background:...
    copy = __copy__

    def settodraw(self, backdround: Background) -> None:...
    def draw(self, surface: Surface | None = None, find: bool = ...) -> None:...
    def add_background(self, backgrounds: Backgrounds) -> None:...
    def remove_background(self, backgrounds: Backgrounds) -> None:...
    def has_background(self, backgrounds: Backgrounds) -> bool:...
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


class CircleButton(RoundButton):
    @overload
    def __init__(
            self,
            size: _Size,
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


class Screen:
    backgrounds: Backgrounds
    rect: Rect
    x: int
    y: int
    top: int
    left: int
    bottom: int
    right: int
    topleft: Tuple[int, int]
    bottomleft: Tuple[int, int]
    topright: Tuple[int, int]
    bottomright: Tuple[int, int]
    midtop: Tuple[int, int]
    midleft: Tuple[int, int]
    midbottom: Tuple[int, int]
    midright: Tuple[int, int]
    center: Tuple[int, int]
    centerx: int
    centery: int
    size: Tuple[int, int]
    width: int
    height: int
    w: int
    h: int
    size: Tuple[int, int]
    flags: Tuple[int]
    def __copy__(self) -> Surface: ...
    def __getattr__(self, item: str) -> Any | None:...
    @staticmethod
    @overload
    def update(
            rectangle: Optional[
                Union[RectValue, Sequence[Optional[RectValue]]]] = None
    ) -> None: ...
    @staticmethod
    @overload
    def update(x: int, y: int, w: int, h: int) -> None: ...
    @staticmethod
    @overload
    def update(xy: _Pos, wh: _Size) -> None: ...
    @staticmethod
    def flip() -> None:...
    copy = __copy__
    
    def blit(
            self,
            source: Surface,
            dest: Union[Coordinate, RectValue],
            area: Optional[RectValue] = None,
            special_flags: int = 0,
    ) -> Rect: ...
    
    def blits(
            self,
            blit_sequence: Sequence[
                Union[
                    Tuple[Surface, Union[Coordinate, RectValue]],
                    Tuple[Surface, Union[Coordinate, RectValue], Union[
                        RectValue, int]],
                    Tuple[Surface, Union[
                        Coordinate, RectValue], RectValue, int],
                ]
            ],
            doreturn: Union[int, bool] = 1,
    ) -> Union[List[Rect], None]: ...
    
    @overload
    def convert(self, surface: Surface) -> Surface: ...
    
    @overload
    def convert(self, depth: int, flags: int = 0) -> Surface: ...
    
    @overload
    def convert(self, masks: ColorValue, flags: int = 0) -> Surface: ...
    
    @overload
    def convert(self) -> Surface: ...
    
    @overload
    def convert_alpha(self, surface: Surface) -> Surface: ...
    
    @overload
    def convert_alpha(self) -> Surface: ...
    
    def fill(
            self,
            color: ColorValue,
            rect: Optional[RectValue] = None,
            special_flags: int = 0,
    ) -> Rect: ...
    
    def scroll(self, dx: int = 0, dy: int = 0) -> None: ...
    
    @overload
    def set_colorkey(self, color: ColorValue, flags: int = 0) -> None: ...
    
    @overload
    def set_colorkey(self, color: None) -> None: ...
    
    def get_colorkey(self) -> Optional[RGBAOutput]: ...
    
    @overload
    def set_alpha(self, value: int, flags: int = 0) -> None: ...
    
    @overload
    def set_alpha(self, value: None) -> None: ...
    
    def get_alpha(self) -> Optional[int]: ...
    
    def lock(self) -> None: ...
    
    def unlock(self) -> None: ...
    
    def mustlock(self) -> bool: ...
    
    def get_locked(self) -> bool: ...
    
    def get_locks(self) -> Tuple[Any, ...]: ...
    
    def get_at(self, x_y: Sequence[int]) -> Color: ...
    
    def set_at(self, x_y: Sequence[int], color: ColorValue) -> None: ...
    
    def get_at_mapped(self, x_y: Sequence[int]) -> int: ...
    
    def get_palette(self) -> List[Color]: ...
    
    def get_palette_at(self, index: int) -> Color: ...
    
    def set_palette(self, palette: Sequence[ColorValue]) -> None: ...
    
    def set_palette_at(self, index: int, color: ColorValue) -> None: ...
    
    def map_rgb(self, color: ColorValue) -> int: ...
    
    def unmap_rgb(self, mapped_int: int) -> Color: ...
    
    def set_clip(self, rect: Optional[RectValue]) -> None: ...
    
    def get_clip(self) -> Rect: ...
    
    @overload
    def subsurface(self, rect: RectValue) -> Surface: ...
    
    @overload
    def subsurface(
            self, left_top: Coordinate, width_height: Coordinate
            ) -> Surface: ...
    
    @overload
    def subsurface(
            self, left: float, top: float, width: float, height: float
    ) -> Surface: ...
    
    def get_parent(self) -> Surface: ...
    
    def get_abs_parent(self) -> Surface: ...
    
    def get_offset(self) -> Tuple[int, int]: ...
    
    def get_abs_offset(self) -> Tuple[int, int]: ...
    
    def get_size(self) -> Tuple[int, int]: ...
    
    def get_width(self) -> int: ...
    
    def get_height(self) -> int: ...
    
    def get_rect(self, **kwargs: Any) -> Rect: ...
    
    def get_bitsize(self) -> int: ...
    
    def get_bytesize(self) -> int: ...
    
    def get_flags(self) -> int: ...
    
    def get_pitch(self) -> int: ...
    
    def get_masks(self) -> RGBAOutput: ...
    
    def set_masks(self, color: ColorValue) -> None: ...
    
    def get_shifts(self) -> RGBAOutput: ...
    
    def set_shifts(self, color: ColorValue) -> None: ...
    
    def get_losses(self) -> RGBAOutput: ...
    
    def get_bounding_rect(self, min_alpha: int = 1) -> Rect: ...
    
    def get_view(self, kind: _ViewKind = "2") -> BufferProxy: ...
    
    def get_buffer(self) -> BufferProxy: ...
    
    def get_blendmode(self) -> int: ...
    
    def premul_alpha(self) -> Surface: ...
    def __init__(
            self,
            size: _Size = ...,
            flag: int = 0,
            *adds: Group | Sprite | Background | Surface,
            depth: int = 0,
            display: int = 0,
            vsync: int = 0,
            resizeable: bool = ...,
    ) -> None:...
    def resize(self, size: _Size) -> None:...
    def add(self, *adds: Group | Sprite | Background | Surface) -> None:...
    def set_image(self, image: Surface) -> None:...
    def mainloop(self, stop_to: _Call, *event: (List | Tuple)[int, _Call]) -> None:...


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

class Login:
    name: str
    password:  str
    automaticlogin: bool
    def __init__(
            self,
            login: Dict[str, str] = {},
            passwordhas: Iterable[str] = ...,
            password_lower: int = 6,
            password_upper: int = 100,
            background: str | None = None,
    ) -> None:...
    def destory(self) -> None:...
    def errorPack(self, value: str) -> None:...
    def login(self) -> None | Tuple[str, str, str, bool]:...

def toKeyboardInterrrupt(command: _Call = _NoneCommand) -> None:...
def terminate(code: Any = 0, command: _Call = _NoneCommand) -> None:...
def toTerminate(code: Any = 0, command: _Call = _NoneCommand) -> _Call:...
def CheckForQuit(minmize: int | None | False = ..., savecommand: _Call = _NoneCommand) -> None:...
def CheckForMinmize(key: int = ...) -> None:...
def CheckForResize(nones: bool = True) -> _Size | None:...
def toList(surf: Surface) -> List[Tuple[int, int, int, int]]:...

colors: Dict[str, Tuple[int, int, int, 255]]
Clock = pygame.time.Clock
clock: Clock
def tick(fps: float = 0) -> float:...
def toColor(color: _Color, raised: bool = True) -> Color:...
