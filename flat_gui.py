__quit = quit

import socket
import threading as _t
from os import getcwd as _getcwd
from os.path import isabs as _isabs, join as _join
from math import atan2 as _at2
import pygame
from pygame import *
from pygame.display import *
from pygame.locals import *

from pyns.file import seek as _seek
from pyns.fm import Angle, DEGREES, RADIANS
from pyns.func import overload as _overload
from pyns.iter import fill as _fill, flatten as _flatten
from pyns.structures import Stack as _Stk
from pyns.url import (
    CHINESE as _c, ERRORCODE as _r, idlang as _il, toPinyin as _tp,
)


quit = __quit

init()
font.init()
mixer.init()
TOP = "top"
BOTTOM = "bottom"
RIGHT = "right"
LEFT = "left"
TOPLEFT = "topleft"
TOPRIGHT = "topright"
BOTTOMLEFT = "bottomleft"
BOTTOMRIGHT = "bottomright"
NONE = "none"
REGISTRATION = "registration"
LOGIN = "login"
FRRT = "free rotating"
FLAR = "flip Left and right"
NRTT = "no rotation"
info = pygame.display.Info()
maxSize = maxWidth, maxHeight = info.current_w, info.current_h


class Sprite(pygame.sprite.Sprite):
    _name = 1
    
    def __len__(self):
        return self.groups().__len__()
    
    def resize(self, size):
        self.old_image = pygame.transform.scale(self.old_image, size)
    
    def angle_collide(self, angle, group, kill=False):
        if angle not in (TOP, BOTTOM, LEFT, RIGHT):
            raise ValueError("angle parameter can't be %s" % angle)
        has = False
        angles_iter = (TOP, RIGHT, BOTTOM, LEFT, TOP, RIGHT)
        for sprite in group:
            angles = {}
            self_angle = getattr(self, angle)
            if angle == TOP:
                angles["other to side"] = sprite.bottom >= self_angle >= sprite.top
                angles["other sides"] = (sprite.left, sprite.right)
                angles["self sides"] = (self.left, self.right)
            elif angle == BOTTOM:
                angles["other to side"] = sprite.top <= self_angle <= sprite.bottom
                angles["other sides"] = (sprite.left, sprite.right)
                angles["self sides"] = (self.left, self.right)
            elif angle == LEFT:
                angles["other to side"] = sprite.right >= self_angle >= sprite.left
                angles["other sides"] = (sprite.top, sprite.bottom)
                angles["self sides"] = (self.top, self.bottom)
            else:
                angles["other to side"] = sprite.left <= self_angle <= sprite.right
                angles["other sides"] = (sprite.top, sprite.bottom)
                angles["self sides"] = (self.top, self.bottom)
            
            if angles["other to side"] and (
                angles["other sides"][0] < angles["self sides"][0]
                    <= angles["other sides"][1] or
                angles["other sides"][0] <= angles["self sides"][1]
                    < angles["other sides"][1]
            ):
                has = True
                setattr(
                    self,
                    angle,
                    getattr(
                        sprite,
                        angles_iter[angles_iter.index(angle) + 2],
                    ),
                )
                break
        return has
    
    def __getattr__(self, item):
        # print(item)
        if item == "image":
            return Surface((1, 1)).convert_alpha()
        if item == "rect":
            return self.image.get_rect()
        if hasattr(self.rect, item):
            # print(1, item)
            return getattr(self.rect, item)
        else:
            return getattr(super(Sprite, self), item)
        
    def __setattr__(self, key, value):
        if not (key == "rect") and hasattr(self.rect, key):
            setattr(self.rect, key, value)
        else:
            super(Sprite, self).__setattr__(key, value)
            
    def touchedge(self, screen_rect, turn_backNone=True):
        """
        :type screen_rect: pygame.Rect
        :return: bool
        """
        if self.colliderect(
                Rect(
                    -1,
                    0,
                    1,
                    screen_rect.height,
                ),
        ):
            return LEFT
        elif self.colliderect(
                Rect(
                    0,
                    -1,
                    screen_rect.width,
                    1
                ),
        ):
            return TOP
        elif self.colliderect(
                Rect(
                    screen_rect.right,
                    0,
                    1,
                    screen_rect.height,
                ),
        ):
            return RIGHT
        elif self.colliderect(
                Rect(
                    0,
                    screen_rect.bottom,
                    screen_rect.width,
                    1,
                ),
        ):
            return BOTTOM
        elif turn_backNone:
            return None
        else:
            return NONE
    
    def bounceatTheedge(self, screen_rect):
        touch = self.touchedge(screen_rect)
        if touch is not None:
            self.set_angle(- self.angle)
            if touch in (LEFT, RIGHT):
                self.angleleft(Angle(DEGREES, 180))
            self.rect.center = self.old_center
    
    def becomeLarger(self, size, speed=1, fps=60):
        for i in range(0, size, speed):
            clock.tick(fps)
            width, height = self.image.get_size()
            width  += speed
            height += speed
            if width > 0 and height > 0:
                self.image = pygame.transform.scale(
                    self.image,
                    (width + speed, height + speed),
                )
            else:
                break
    
    def becomeSmaller(self, size, speed=1, fps=60):
        self.becomeLarger(- size, - speed, fps)
    
    @_overload
    def set_angle(self, a0):
        if isinstance(a0, Angle):
            self.angle = a0
        elif isinstance(a0, pygame.sprite.Sprite):
            self.set_angle(a0.rect.topleft)
        else:
            self.set_angle(a0[0], a0[1])
    
    @_overload
    def set_angle(self, arg1, arg2):
        if arg1 in (DEGREES, RADIANS):
            self.angle = Angle(arg1, arg2)
        else:
            self.angle = Angle(RADIANS, _at2(self.centery - arg2, arg1 - self.centerx))
    
    @_overload
    def angleright(self, angle):
        self.set_angle(self.angle - angle)
    
    @_overload
    def angleright(self, types, number):
        self.angleright(Angle(types, number))
    
    @_overload
    def angleleft(self, angle):
        self.set_angle(self.angle + angle)
    
    @_overload
    def angleleft(self, types, number):
        self.angleleft(Angle(types, number))
        
    def _alpha(self, alpha):
        def near(a, b):
            return abs(a - b) <= 5
        alpha = toColor(alpha)
        for x in range(self.width):
            for y in range(self.height):
                r, g, b, a = self.image.get_at((x, y))
                if near(r, alpha.r) and near(g, alpha.g) and near(b, alpha.b):
                    self.image.set_at((x, y), (0, 0, 0, 0))
    
    def alpha(self, alpha):
        _t.Thread(
            target=self._alpha,
            name="%s alpha tread" % self.name,
            args=(alpha,),
            daemon=True,
        ).start()

    def set_image(self, image, size=None, alpha=None):
        """
        :param image:
            Sprite: inherit,
            str: open file or open color,
            color(list or tuple): set the color surface,
            surface: set the surface,
            NoneType: new surface(color: black)
        :param size:
            List[width: int, height: int] | Tuple[width: int, height: int]
        :param alpha: Color | None
        :return: None
        :transform size:
            width: None,
            height: None,
            (if value size is none)
        :raises:
            if image is color | None and _size is None to raise ValueError
                _size parameter can't be None
            if image is file and can't find the file to raise ValueError
                The image parameter file can't be found
        """
        if image is False:
            self.resize(size)
            return
        if isinstance(image, Sprite):
            self.image = image.image
            if size is not None:
                self.image = pygame.transform.scale(self.image, size)
            self.rect = image.rect
            return
        if isinstance(image, str):
            if toColor(image, False) is not image or isinstance(
                    image, Color):
                if size is None:
                    raise ValueError("_size parameter can't be None")
                self.image = pygame.Surface(size).convert_alpha()
                self.image.fill(toColor(image))
            else:
                if not _isabs(image):
                    image = _join(_getcwd(), image)
                try:
                    if image.lower().endswith(".gif"):
                        # 打开动图（未完成）
                        # 想法：先把GIF图像分成N个静图再依次打开
                        # 可以调用函数的isinstance(image, (list, tuple))
                        pass
                    else:
                        self.image = pygame.image.load(image).convert_alpha()
                    
                    if size is not None:
                        self.image = pygame.transform.scale(
                            self.image, size
                            )
                except FileNotFoundError:
                    raise ValueError(
                        "The image parameter file can't be found: %s" %
                        image)
        elif isinstance(image, (list, tuple)):
            if all(isinstance(file, (str, Surface)) for file in image):
                # 打开多个图片（未完成）
                # 想法：依次打开（需要在update的时候切换
                pass
            if len(image) == 2:
                self.set_image(None, image, alpha=alpha)
                return
            if size is None:
                raise ValueError("size parameter can't be None")
            self.image = pygame.Surface(size).convert_alpha()
            self.image.fill(image)
        elif isinstance(image, Surface):
            self.image = image.convert_alpha()
        elif image is None:
            if size is None:
                raise ValueError("_size parameter can't be None")
            self.image = pygame.Surface(size).convert_alpha()
        else:
            raise ValueError(
                "The image parameter isn't recognized: %s" % image)

        if hasattr(self, "rect"):
            topleft = self.rect.topleft
        else:
            topleft = (0, 0)
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft
        if alpha:
            self.alpha(alpha)

    def __init__(
            self,
            image=None,
            size=None,
            angle=Angle(RADIANS, 0),
            filp_mode=FRRT,
            *groups,
    ):
        super(Sprite, self).__init__(*groups)
        self.name = "%s object(number: %d)" % (self.__class__.__name__, self._name)
        self.__class__._name += 1
        self.set_image(image, size)
        self.old_image = self.image.copy()
        self.set_angle(angle)
        self._stop = False
        self._suspend = False
        self.flip_mode=filp_mode
        self.old_center = (100, 100)
    
    def forward(self, toForward):
        toX, toY = self.angle.cos(), self.angle.sin()
        self.old_center = self.center
        self.rect.x += toX * toForward
        self.rect.y -= toY * toForward
    
    def backword(self, toBackword):
        self.forward(-toBackword)

    def update(self, *args, **kwargs):
        if not (args or kwargs):
            self.image = pygame.transform.rotate(
                self.old_image, self.angle
                )
            center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = center
            return self.rect.topleft
        x = y = None
        try:
            x, y = args
        except:
            if len(kwargs) + len(args) == 2:
                x = y = -1
                if "x" in kwargs:
                    x = kwargs["x"]
                if "y" in kwargs:
                    y = kwargs["y"]
                elif "x" not in kwargs:
                    return
                if args:
                    if x == -1:
                        x = args[0]
                    elif y == -1:
                        y = args[0]
            else:
                return
        if x is None and y is None:
            return self.rect.topleft
        if y is None:
            try:
                self.set_image(x)
            except ValueError:
                self.rect.topleft = x
            else:
                center = self.rect.center
                self.old_image = self.image.copy()
                self.image = pygame.transform.rotate(
                    self.old_image,
                    self.angle,
                )
                self.rect = self.image.get_rect()
                self.rect.center = center
        if not (isinstance(x, int) and isinstance(y, int)):
            return
        if self.flip_mode == FRRT:
            self.image = pygame.transform.rotate(self.old_image, self.angle.degrees)
        elif self.flip_mode == FLAR and self.angle.degrees > 180:
            self.image = pygame.transform.flip(
                self.old_image, True, False)
        else:
            self.image = self.old_image.copy()
        self.old_center = self.center
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    
    def copy(self):
        temp = self.__class__(
            self.image, None, 0, *self.groups())
        temp.set_angle(self.angle)
        return temp
    
    __copy__ = copy
    
    def __add__(self, other):
        new = self.copy()
        new += other
        return new
        
    def __iadd__(self, other):
        if isinstance(other, pygame.sprite.Sprite):
            self.image.blit(other.image, other.rect)
        elif isinstance(other, Angle):
            self.angleleft(other)
        elif isinstance(other, (list, tuple)):
            x, y = other
            self.rect.x += x
            self.rect.y += y
        elif isinstance(other, Rect):
            self.rect.x += other.x
            self.rect.y = other.y
        return self
    
    def __sub__(self, other):
        new = self.copy()
        new -= other
        return new
    
    def __isub__(self, other):
        if isinstance(other, Sprite):
            raise AttributeError("other can't be Sprite")
        elif isinstance(other, int):
            self.angleright(other)
        elif isinstance(other, (list, tuple)):
            x, y = other
            self.rect.x -= x
            self.rect.y -= y
        return self
    
    def __getattr__(self, item):
        if item == "rect":
            return Rect(0, 0, 1, 1)
        elif hasattr(self.rect, item):
            return getattr(self.rect, item)
        elif item == "xy":
            return self.topleft
        else:
            raise AttributeError("Text object has not attribute " + item)
    
    def __setattr__(self, key, value):
        if hasattr(self.rect, key):
            setattr(self.rect, key, value)
        else:
            super(Sprite, self).__setattr__(key, value)
    
    rectangle = property(lambda self: self.angle, set_angle)


class Button(Sprite):
    def __init__(
            self,
            size,
            text,
            command=lambda: None,
            color=(255, 255, 255, 0),
            *groups,
            image=None,
            text_color=(0, 0, 0),
            font=None,
    ):
        super(Button, self).__init__(color, size, *groups)
        self.old_image = self.image.copy()
        temp = max(text.split("\n"), key=lambda txt: len(txt))
        temp = len(temp)
        temp = max(temp, 2)
        temp = size[0] / temp * 2
        temp = round(temp)
        self.text = Text(
            temp,
            text,
            text_color,
            font,
        )
        self.text.rect.center = self.rect.center
        self.command = command
        self._key = None
    
    def bind(self, key=None):
        if key:
            self._key = key
        else:
            return self._key
    
    def touch(self, pos=None):
        if not pos:
            pos = pygame.mouse.get_pos()
        return self.collidepoint(pos)
        
    def click(self, pos=None):
        if not self.touch(pos):
            return False
        for upEvent in event.get(MOUSEBUTTONUP):
            return upEvent.button
        return None
    
    def update(
        self,
        text=None,
        text_color=None,
        color=None,
    ):
        self.text.update(text, text_color)
        temp = self.click()
        if temp:
            try:
                self.command(temp)
            except TypeError:
                self.command()
        for event in pygame.event.get(KEYUP):
            if event.key == self._key:
                self.command()
                return
        if color:
            self.set_image(color, self.image.get_size())
        self.image = self.old_image.copy()
        self.image.blit(self.text.image, self.text.rect)


Group = pygame.sprite.Group
Surface = pygame.Surface
Rect = pygame.Rect


class Background:
    def backgrounds(self):
        return tuple(self.background_groups)

    def groups(self):
        return tuple(self.__groups)

    def __iter__(self):
        return iter(self.groups())

    def __len__(self):
        return max(len(self.__groups) - int(bool(self.background)), 0)

    def add_group(self, group):
        if not self.has_group(group):
            self.__groups.append(group)

    def remove_group(self, group):
        if self.has_group(group):
            self.__groups.remove(group)

    def has_group(self, group):
        return group in self.__groups

    def add(self, *backgroundses):
        for backgrounds in backgroundses:
            if isinstance(backgrounds, Backgrounds):
                self.add_backgrounds(backgrounds)
                backgrounds.add_background(self)
                continue
            elif isinstance(backgrounds, Group):
                self.add_group(backgrounds)
                continue

            try:
                self.add(*backgrounds)
            except:
                if hasattr(backgrounds, "to_iter"):
                    for bakcground in backgrounds:
                        self.add(background)
                    continue
                elif isinstance(backgrounds, pygame.Surface):
                    self.add(Group(Sprite(backgrounds)))
                    continue
                elif isinstance(backgrounds, pygame.sprite.Sprite):
                    self.add(Group(backgrounds))
                    continue
                elif hasattr(backgrounds, "__iter__"):
                    for bakcground in backgrounds:
                        self.add(background)
                    continue
    
    def __contains__(self, item):
        return item in (*self.__groups, *self.background_groups)
    
    def draw(self, surface=None):
        if surface is None:
            if self.surface is None:
                raise ValueError("surface parameter can't be None")
            surface = self.surface
        if self.background:
            self.background.draw(surface)
            self.remove(self.background)
        for group in self.__groups:
            group: Group
            group.draw(surface)
        if self.background:
            self.add(self.background)

    def remove(self, *backgroundses):
        for backgrounds in backgroundses:
            if isinstance(backgrounds, Background):
                self.remove_backgrounds(backgrounds)
                backgrounds.remove_background(self)
                continue
            elif isinstance(backgrounds, Group):
                self.remove_group(backgrounds)
                continue

            try:
                self.remove(*backgrounds)
            except:
                if hasattr(backgrounds, "to_iter"):
                    for background in backgrounds.to_iter():
                        self.remove(background)
                    continue
                elif hasattr(backgrounds, "__iter__"):
                    for bakcground in backgrounds:
                        self.remove(background)
                    continue

    def add_backgrounds(self, backgrounds):
        if not self.has_backgrounds(backgrounds):
            self.background_groups.append(backgrounds)

    def remove_backgrounds(self, backgrounds):
        if self.has_backgrounds(backgrounds):
            self.background_groups.remove(backgrounds)

    def has_backgrounds(self, backgrounds):
        return backgrounds in self.background_groups

    def __repr__(self):
        return "%s object (has %i Groups, in %i Backgroundses)" % (
            self.__class__.__name__,
            len(self),
            len(self.backgrounds()),
        )

    def __init__(self, surface, background=None, *groups):
        self.surface = surface
        if (
                isinstance(background, (list, tuple, pygame.Color)) or
                toColor(background) != background
        ):
            new = Surface(surface.get_size())
            new.fill(background)
            background = new
        if background is not None:
            self.background = Sprite(background)
            self.spritebackground = self.background
            self.background.image = pygame.transform.scale(
                self.background.image,
                surface.get_size(),
            )
            self.background = Group(self.background)
        else:
            self.background = None
            self.spritebackground = None
        self.background_groups = []
        self.__groups = []
        self.add(*groups)
        if background:
            self.add(self.background)

    def update(self, *args, **kw):
        if self.background:
            self.remove(self.background)
            self.spritebackground.image = pygame.transform.scale(
                self.spritebackground.image,
                self.surface.get_size(),
            )
            self.spritebackground.update(0, 0)

        for group in self.groups():
            group.update(*args, **kw)

        if self.background:
            self.add(self.background)

    def copy(self):
        return self.__class__(
            self.surface,
            self.background.sprites()[0].image,
            self.groups()
        )

    __copy__ = copy


default_background = None


def setDefaultbackground(background):
    global default_background
    default_background = background


class Backgrounds:
    def __copy__(self):
        return self.__class__(self.backgrounds)

    copy = __copy__

    def settodraw(self, background):
        if background in self.backgrounds:
            self.default_background = background

    def __toRaise(self):
        raise AttributeError(
            "default_background of Backgrounds object attribute can't be None"
        )
    
    def __contains__(self, item):
        return item in self.backgrounds
    
    def draw(self, surface=None, find=True):
        if (not self.default_background) and find:
            if self.backgrounds:
                self.default_background = self.backgrounds[0]
            elif default_background:
                self.settodraw(default_background)
        if self.default_background is not None:
            self.default_background.draw(surface)
        else:
            self.__toRaise()

    def __repr__(self):
        return "%s object has %i Background" % (
            self.__class__.__name__,
            len(self)
        )

    def __iter__(self):
        return iter(self.backgrounds)

    def __len__(self):
        return len(self.backgrounds)

    def __init__(self, *backgrounds):
        self.backgrounds = []
        self.default_background = None
        self.add(*backgrounds)

    def add_background(self, background):
        if not self.has_background(background):
            self.backgrounds.append(background)

    def remove_background(self, background):
        if self.has_background(background):
            self.backgrounds.remove(background)

    def has_background(self, background):
        return background in self.backgrounds

    def add(self, *backgrounds):
        for background in backgrounds:
            if isinstance(background, Background):
                self.add_background(background)
                background.add_backgrounds(self)
                continue
            if isinstance(background, Surface):
                self.add_background(Background(background))
                continue
            try:
                self.add(*background)
            except:
                if hasattr(background, "to_iter"):
                    self.add(background.to_iter())
                if hasattr(background, "__iter__"):
                    for backgroundn in background:
                        self.add(backgroundn)
                raise

    def remove(self, *backgrounds):
        for background in backgrounds:
            if isinstance(background, Background):
                self.remove_background(background)
                background.remove_backgrounds(self)
            try:
                self.remove(*background)
            except:
                if hasattr(background, "to_iter"):
                    self.remove(background.to_iter())
                raise


# Text class
class Text(Sprite):
    def set_text(self, text):
        """
        :param text: Any(has __repr__ or __str__ func) | str
        :return: None
        """
        if text is not None:
            self.text = text
            self.image = self.font.render(str(text), True, self.color, None)
            xy = self.rect.topleft
            self.rect = self.image.get_rect()
            self.rect.topleft = xy

    def __init__(
            self,
            font_size,
            text="",
            color=(255, 255, 255),
            font=None,
            *groups,
    ):
        super(Text, self).__init__(None, (1, 1), (255, 255, 255, 0), *groups)
        if font is not None:
            old_font = font
            # temp = _il(font, _r)
            # if temp == _c:
            #     font = _tp(font)[0]
            font = _seek(
                font,
                r"C:\Windows\Fonts",
                findone=True,
            )
        else:
            old_font = font
        self.color = Color(toColor(color))
        try:
            self.font = pygame.font.Font(font, font_size)
        except pygame.error:
            try:
                self.font = pygame.font.SysFont(old_font, font_size)
            except pygame.error:
                self.font = pygame.font.SysFont(font, font_size)
        self.text = ""
        self.set_text(text)

    def update(self, text=None, color=None, x=None, y=None):
        if x:
            if y is None:
                x, y = x
            self.rect.x = x
            self.rect.y = y
        if color is not None:
            self.color = color
        self.set_text(text)


class RoundedRect(Sprite):
    def __init__(self, *args, **kwargs):
        super(Sprite, self).__init__()
        self.draw(*args, **kwargs)
    
    def update(self, *args, **kwargs):
        if args and kwargs:
            self.draw(*args, **kwargs)
        else:
            return self.topleft
    
    def draw(self, color, round, *rect, width=0, side_color=None):
        color = toColor(color)
        if width > 0:
            side_color = toColor(side_color)
        elif width < 0:
            raise ValueError("width parameter can't less than 0")
        rect = _flatten(rect)
        self.image = Surface(rect).convert_alpha()
        self.image.fill((255, 255, 255, 0))
        topleft = self.topleft
        self.rect = self.image.get_rect()
        self.topleft = topleft
        temp = Rect((0, 0), rect)
        draw.rect(self.image, color, temp, 0, round)
        if width > 0:
            draw.rect(self.image, side_color, temp, width, round)


class RoundButton(RoundedRect, Button):
    def __init__(
            self,
            size,
            round_size,
            text,
            fillcolor,
            command=lambda: None,
            *groups,
            width=0,
            sidecolor=None,
            textcolor="black",
    ):
        Button.__init__(
            self,
            size,
            text,
            command,
            (255, 255, 255, 0),
            *groups,
            text_color=textcolor,
        )
        self.fillcolor = fillcolor
        self.round_size = round_size
        self.side_width = width
        self.sidecolor = sidecolor
        self.draw(fillcolor, round_size, size, width=width, side_color=sidecolor)
    
    def update(self, *args, **kw):
        RoundedRect.update(
            self,
            self.fillcolor,
            self.round_size,
            self.size,
            width=self.side_width,
            side_color=self.sidecolor,
        )
        temp = self.image
        Button.update(self, *args, **kw)
        temp.blit(self.image, (0, 0))
        self.image = temp


class RoundEdgeButton(RoundButton):
    def __init__(self, size, length, *args, **kw):
        super().__init__(
            size,
            (
                (size[0] - length) / 2,
                size[1] / 2,
            ),
            *args,
            **kw,
        )


class CircleButton(RoundButton):
    def __init__(self, size, *args, **kw):
        super().__init__((size, size), size, *args, **kw)


class Screen:
    def __init__(
            self,
            size=(0, 0),
            flag=0,
            *adds,
            depth=0,
            display=0, vsync=0, resizeable=False):
        self.flags = (
            flag | RESIZABLE if resizeable else flag, depth, display, vsync)
        self.resize(size)
        self.backgrounds = Backgrounds(*adds)
        for background in self.backgrounds:
            background.surface = self.mode
        self.resizeable = resizeable
    
    def __getattr__(self, item):
        if hasattr(self, "mode") and self.mode and hasattr(self.mode, item):
            return getattr(self.mode, item)
        elif hasattr(pygame.display, item):
            return getattr(pygame.display, item)
        elif hasattr(self.rect, item):
            return getattr(self.rect, item)
        else:
            raise AttributeError("Screen object has not attribute %s" % item)
        
    def resize(self, size):
        self.size = self.width, self.height = size
        self.mode = set_mode(size, *self.flags)
        self.rect = self.get_rect()
    
    def set_background(self, image):
        for background in self.backgrounds:
            background.background = image
        
    def add(self, *adds):
        self.backgrounds.add(*adds)
    
    def mainloop(self, stop_to, *events):
        try:
            while True:
                CheckForQuit(save_command=stop_to)
                newsize = CheckForResize()
                if self.resizeable and newsize is not None:
                    self.resize(newsize)
                for event in get(tuple(map(lambda evn: evn[0], events))):
                    command = None
                    for evnt, com in events:
                        if evnt == event.type:
                            command = com
                            break
                    try:
                        command()
                    except (TypeError, ValueError):
                        command(event)
                    except KeyboardInterrupt:
                        toKeyboardInterrrupt(stop_to)
                    except SystemExit:
                        raise
                    except:
                        __tb.print_exc()
                update()
        except KeyboardInterrupt:
            toKeyboardInterrrupt(stop_to)


class Barrage(Sprite):
    def __init__(
            self,
            text,
            size=(100, 50),
            color=(0, 0, 0, 255),
            text_color=(100, 100, 100, 255),
            speed=1,
            yspeed=10,
    ):
        super().__init__(None, size)
        self.text = Text(
            round(size[0] / len(text) * 2 if size[0] <= size[1] else size[1] - 10),
            text,
            text_color,
        )
        self.image = Surface(size).convert_alpha()
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.text.rect.center = self.center
        self.image.blit(self.text.image, self.text.rect)
        self.width, self.height = size
        self.speed = speed
        self.yspeed = yspeed
    
    def update(self, speed=None):
        _pixel = pygame.PixelArray(self.image)
        if speed is None:
            speed = self.speed
        for x in range(self.width):
            for y in range(self.height):
                r, g, b, a = self.image.get_at((x, y))
                a -= speed
                if a <= 0:
                    self.kill()
                    return
                _pixel[x][y] = Color(r, g, b, a)
        self.y -= self.yspeed
        del _pixel


class Loading(Sprite):
    def __init__(self, size=None, shape=0):
        if isinstance(size, (int, float)):
            size = (size, size)
        elif size is None:
            size = get_desktop_sizes()[0]
        super().__init__((0, 0, 0, 0), size)


class Login:
    @property
    def name(self):
        return self.nameText.get()
    
    @name.setter
    def name(self, value):
        self.nameText.set(value)
    
    @property
    def password(self):
        return self.passwordText.get()
    
    @password.setter
    def password(self, value):
        self.passwordText.set(value)
    
    @property
    def automaticlogin(self):
        return self.amlVar.get()
    
    @automaticlogin.setter
    def automaticlogin(self, value):
        self.amlVar.set(value)
    
    def __init__(
            self,
            logins={},
            passwordhas=("letters", "digits"),
            passwordlower=6,
            passwordupper=100,
            showaml=True,
            background=None,
    ):
        self.passwordhas = passwordhas
        self.passwords = (passwordlower, passwordupper)
        if isinstance(logins, (tuple, list)):
            if isinstance(logins[0], str):
                if isinstance(logins[1], str):
                    bind, send = (logins[0], 80), logins[1]
                else:
                    bind, send = (
                        logins,
                        "GET HTTP/1.0\r\nHost: %s\r\n\r\n" % logins[0],
                    )
            else:
                logins = _flatten(logins)
                bind, send = (logins[:2], logins[2])
            network_socket = socket.socket()
            network_socket.bind(bind)
            network_socket.sendall(
                send.encode("utf-8") if isinstance(send, str) else send)
        self.logins = logins
        import tkinter as tk
        self.logined = {}
        self.tk = tk.Tk()
        self.tk.title("登录")
        self.background = tk.Label(self.tk, image=tk.PhotoImage(background))
        self.background.place(x=0, y=0)
        self.dFrame = tk.Frame(
            self.tk,
        )
        self.labelFrame = tk.Frame(
            self.dFrame,
        )
        self.entryFrame = tk.Frame(
            self.dFrame,
        )
        self.nameLabel = tk.Label(
            self.labelFrame,
            text="用户名：",
        )
        self.nameText = tk.StringVar(self.entryFrame)
        self.nameEntry = tk.Entry(
            self.entryFrame,
            textvariable=self.nameText,
        )
        self.passwordLabel = tk.Label(
            self.labelFrame,
            text=" 密码：",
        )
        self.passwordText = tk.StringVar(self.entryFrame)
        self.passwordEntry = tk.Entry(
            self.entryFrame,
            textvariable=self.passwordText,
        )

        self.nameLabel.pack(padx=10, pady=10)
        self.passwordLabel.pack(padx=10, pady=10)
        self.nameEntry.pack(padx=10, pady=10)
        self.passwordEntry.pack(padx=10, pady=10)
        self.labelFrame.pack(side=LEFT)
        self.entryFrame.pack(side=RIGHT)
        self.dFrame.pack(padx=150, pady=30)
        
        self.errorText = tk.StringVar(self.dFrame)
        self.errorLabel = tk.Label(
            self.entryFrame,
            textvariable=self.errorText,
            fg="red",
        )
        self.gridErrorLabel = tk.Label(
            self.labelFrame,
        )
        
        self.dButtons = tk.Frame(self.tk)
        
        self.dButton = tk.Button(
            self.dButtons,
            text="登录/注册",
            command=self.login,
        )
        self.dButton.bind("<Return>", self.login)
        
        self.dButton.pack(side=LEFT, padx=25)
        
        self.amlVar = tk.BooleanVar(self.tk)
        self.amlButton = tk.Checkbutton(
            self.dButtons,
            text="自动登录",
            variable=self.amlVar,
        )
        
        self.amlButton.pack(side=RIGHT, padx=25)
        
        self.dButtons.pack(pady=30)
        
        self.tk.protocol("WM_DELETE_WINDOW", self.destory)
        try:
            self.tk.mainloop()
        except KeyboardInterrupt:
            toKeyboardInterrrupt()
        if self.logined == {}:
            exit(1)
    
    def destory(self):
        if self.logined:
            self.tk.destroy()
        else:
            from tkinter import messagebox
            inputs = messagebox.askyesnocancel(
                "登录",
                "您还未登录，是否登录？",
            )
            if inputs:
                self.login()
            elif inputs is not None:
                if messagebox.askyesno(
                    "登录",
                    "是否退出？",
                    default=messagebox.NO,
                ):
                    self.tk.destroy()
    
    def errorPack(self, value):
        self.errorText.set(str(value))
        self.errorLabel.pack(side=BOTTOM)
        self.gridErrorLabel.pack(side=BOTTOM)
    
    def login(self):
        import string
        from tkinter import messagebox
        canInput = ""
        for has in self.passwordhas:
            if hasattr(string, has):
                canInput += getattr(string, has)
            else:
                canInput += getattr(string, "ascii_" + has)
        try:
            self.errorLabel.pack_info()
        except:
            pass
        try:
            self.gridErrorLabel.pack_info()
        except:
            pass
        if self.name == "":
            self.errorPack("用户名为空")
        elif self.password == "":
            self.errorPack("密码为空")
        elif not self.passwords[0] <= len(self.password) <= self.passwords[1]:
            self.errorPack("密码长度不符合要求（%d ≤ 密码长度 ≤ %d）" % self.passwords)
        elif any(char not in canInput for char in self.password):
            self.errorPack("密码文字不符合要求（密码必须是字母或者数字）")
        elif self.name not in self.logins:
            self.tk.title("注册")
            self.tk.update()
            if messagebox.askokcancel("注册", "是否注册？"):
                self.logined = {
                    "state"   : REGISTRATION,
                    "username": self.name,
                    "password": self.password,
                    "aml"     : self.automaticlogin,
                }
                self.destory()
                return self.logined
            else:
                self.tk.title("登录")
        elif self.logins[self.name] == self.password:
            self.logined = {
                "state"   : LOGIN,
                "username": self.name,
                "password": self.password,
                "aml"     : self.automaticlogin,
            }
            self.destory()
            return self.logined
        else:
            self.errorPack("用户名和密码不匹配")


def toKeyboardInterrrupt(command=lambda: None):
    terminate(-1073741510, command)
    
    
def terminate(code=0, command=lambda: None):
    # save the thread
    command()
    # screen.quit
    pygame.quit()
    # system.exit
    import sys
    sys.exit(code)


def toTerminate(code=0, command=lambda: None):
    return lambda: terminate(code, command)


def CheckForQuit(minmize=K_F10, savecommand=lambda: None):
    for quit_event in pygame.event.get((QUIT, KEYUP)):
        if quit_event.type == QUIT or quit_event.key == K_ESCAPE:
            terminate(0, savecommand)
        elif minmize and quit_event.key == minmize:
            iconify()
        else:
            pygame.event.post(quit_event)


def CheckForMinmize(key=K_F10):
    for minmize_event in pygame.event.get(KEYUP):
        if minmize_event.key == key:
            iconify()
        else:
            pygame.event.post(minmize_event)


def toColor(color, raised=True):
    if color is None:
        if raised:
            raise ValueError("color value can't be None")
        else:
            return None
    if isinstance(color, Color):
        return color
    elif color == WHITE:
        return Color(255, 255, 255)
    else:
        try:
            return Color(color)
        except (ValueError, TypeError):
            if raised:
                raise ValueError("Unrecognized color parameter") from None
            else:
                return color


def CheckForResize(nones=True):
    for resize_event in pygame.event.get(VIDEORESIZE):
        return resize_event.size
    return None if nones else get_surface().get_size()


def toList(surf):
    temp = []
    width, height = surf.get_size()
    _fill(temp, (width, height))
    for x in range(width):
        for y in range(height):
            temp[x][y] = surf.get_at((x, y))
    return temp


_timer = pygame.USEREVENT


def timer(*args, **kwargs):
    global _timer
    _timer += 1
    pygame.time.set_timer(_timer, *args, **kwargs)
    return _timer


Color = pygame.Color
pygame_Sprite = pygame.sprite.Sprite
Clock = pygame.time.Clock
clock = Clock()
tick = clock.tick
WHITE  = "white"
BLACK  = "black"
RED    = "red"
BLUE   = "blue"
GREEN  = "green"
ORANGE = "orange"
