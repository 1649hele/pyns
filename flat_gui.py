__quit = quit

import threading as _t
from os import getcwd as _getcwd
from os.path import isabs as _isabs, join as _join
from math import atan2 as _at2
import pygame
from pygame import *
from pygame.display import *
from pygame.locals import *
import pygamePhysics as physics
import pygame.mask as collide

try:
    from .file import seek as _seek
    from .fm import Angle, DEGREES, RADIANS
    from .func import overload as _overload
    from .iter import fill as _fill, flatten as _flatten
    from .structures import Stack as _Stk
    from .url import (
        CHINESE as _c, ERRORCODE as _r, idlang as _il, toPinyin as _tp,
    )
except ImportError:
    from file import seek as _seek
    from fm import Angle, DEGREES, RADIANS
    from func import overload as _overload
    from iter import fill as _fill, flatten as _flatten
    from structures import Stack as _Stk
    from url import (
        CHINESE as _c, ERRORCODE as _r, idlang as _il, toPinyin as _tp,
    )

import easygui as _eg


quit = __quit
get_screen = set_mode

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
FRRT = "free rotating"
FLAR = "flip Left and right"
NRTT = "no rotation"
info = pygame.display.Info()
maxSize = maxWidth, maxHeight = info.current_w, info.current_h
game_title = "game"
game_icontitle = None
game_icon = None
colors = color.THECOLORS


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
        if item == "image":
            return Surface((1, 1)).convert_alpha()
        if item == "rect":
            return self.image.get_rect()
        if hasattr(self.rect, item):
            return getattr(self.rect, item)
        else:
            try:
                return getattr(super(Sprite, self), item)
            except AttributeError:
                raise AttributeError("%s object as not attribute %s" % (self.__class__.__name__, item))
        
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
            self.old_image = image.old_image
            if size is not None:
                self.old_image = pygame.transform.scale(
                    self.old_image, size
                    )
            self.rect = image.rect
            return
        if isinstance(image, str):
            if toColor(image, False) is not image or isinstance(
                    image, Color
            ):
                if size is None:
                    raise ValueError("_size parameter can't be None")
                self.old_image = pygame.Surface(size).convert_alpha()
                self.old_image.fill(toColor(image))
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
                        self.old_image = pygame.image.load(
                            image
                            ).convert_alpha()
                    
                    if size is not None:
                        self.old_image = pygame.transform.scale(
                            self.old_image, size
                        )
                except FileNotFoundError:
                    raise ValueError(
                        "The image parameter file can't be found: %s" %
                        image
                    )
        elif isinstance(image, (list, tuple)):
            if all(isinstance(file, (str, Surface)) for file in image):
                # 打开多个图片（未完成）
                # 想法：依次打开（需要在update的时候切换）
                pass
            if len(image) == 2:
                self.set_image(None, image, alpha=alpha)
                return
            if size is None:
                raise ValueError("size parameter can't be None")
            self.old_image = pygame.Surface(size).convert_alpha()
            self.old_image.fill(image)
        elif isinstance(image, Surface):
            self.old_image = image.convert_alpha()
        elif image is None:
            if size is None:
                raise ValueError("_size parameter can't be None")
            self.old_image = pygame.Surface(size).convert_alpha()
        else:
            raise ValueError(
                "The image parameter isn't recognized: %s" % image
            )
        
        if hasattr(self, "rect"):
            topleft = self.rect.topleft
        else:
            topleft = (0, 0)
        self.rect = self.old_image.get_rect()
        self.rect.topleft = topleft
        if alpha:
            self.alpha(alpha)
        Sprite.update(self)

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
        self.set_angle(angle)
        self._stop = False
        self._suspend = False
        self.flip_mode=filp_mode
        self.old_center = (100, 100)
        self.set_image(image, size)
    
    def forward(self, toForward):
        toX, toY = self.angle.cos(), self.angle.sin()
        self.old_center = self.center
        self.rect.x += toX * toForward
        self.rect.y -= toY * toForward
    
    def backword(self, toBackword):
        self.forward(-toBackword)

    @_overload
    def update(self):
        if self.flip_mode == FRRT:
            self.image = pygame.transform.rotate(self.old_image, self.angle.degrees)
        elif self.flip_mode == FLAR and self.angle.degrees > 180:
            self.image = pygame.transform.flip(
                self.old_image, True, False)
        else:
            self.image = self.old_image.copy()
        self.old_center = self.center
        self.rect = self.image.get_rect()
        self.rect.center = self.old_center
    
    @_overload
    def update(self, x, y):
        if not (isinstance(x, int) and isinstance(y, int)):
            raise TypeError("x and y must be int")
        self.rect.topleft = (x, y)
        Sprite.update(self)
    
    @_overload
    def update(self, xy):
        Sprite.update(self, xy[0], xy[1])
    
    @_overload
    def update(self, *args, **kwargs):
        self.set_image(*args, **kwargs)
        Sprite.update(self)
    
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
    
    @_overload
    def blit(self, sprite):
        if not (hasattr(sprite, "image") and hasattr(sprite, "rect")):
            raise TypeError("sprite object has not image or rect")
        self.blit(sprite.image, sprite.rect)
    
    @_overload
    def blit(self, image, rect):
        self.old_image.blit(image, rect)
        self.update()
        
    rectangle = property(lambda self: self.angle, set_angle)


def check_mouse(sprite, op=None):
    while hasattr(sprite, "rect"):
        sprite = sprite.rect
    temp = sprite.colliderect(Rect(mouse.get_pos(), (1, 1)))
    if op is None:
        return temp
    elif temp:
        for event in pygame.event.get(op):
            if sprite.colliderect(Rect(event.pos, (1, 1))):
                pygame.event.post(event)
                return event
    return None


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
            center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = center

    def __init__(
            self,
            font_size,
            text="",
            color=(255, 255, 255),
            font=None,
            *groups,
    ):
        super(Text, self).__init__(None, (1, 1), (255, 255, 255, 0), FRRT, *groups)
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
        if font is None:
            try:
                self.font = pygame.font.Font(old_font, round(font_size))
            except:
                self.font = pygame.font.SysFont(old_font, round(font_size))
        else:
            try:
                self.font = pygame.font.Font(font, round(font_size))
            except:
                self.font = pygame.font.SysFont(font, round(font_size))
        self.text = ""
        self.set_text(text)
    
    @_overload
    def update(self, text=None, color=None):
        if color is not None:
            self.color = color
        self.set_text(text)
    
    @_overload
    def update(self, text=None, color=None, xy=(None, None)):
        super(Text, self).update(xy[0], xy[1])
        if color is not None:
            self.color = color
        self.set_text(text)
    
    @_overload
    def update(self, text=None, color=None, x=None, y=None):
        super(Text, self).update(x, y)
        if color is not None:
            self.color = color
        self.set_text(text)

class RoundedRect(Sprite):
    def __init__(self, *args, **kwargs):
        super(Sprite, self).__init__()
        self.draw(*args, **kwargs)
    
    def update(self, *args, **kwargs):
        self.draw(*args, **kwargs)
    
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


class Circle(Sprite):
    def __init__(self, diameter, color, *args, **kwargs):
        color = toColor(color)
        _surface = surface.Surface((diameter, diameter), SRCALPHA)
        _surface.fill((255, 255, 255, 0))
        draw.circle(_surface, color, (diameter/2, diameter/2), diameter/2, *args, **kwargs)
        super(Circle, self).__init__(_surface)


class CircleButton(RoundButton):
    def __init__(self, diameter, *args, **kw):
        super(RoundButton, self).__init__((diameter, diameter), diameter, *args, **kw)


def toKeyboardInterrrupt(command=lambda: None):
    terminate(-1073741510, command)
    
    
def terminate(code=0, command=lambda: None):
    command()
    pygame.quit()
    pygame.mixer.quit()
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
    elif color in colors:
        return Color(colors[color])
    else:
        try:
            return Color(color)
        except (ValueError, TypeError):
            if raised:
                raise ValueError("Unrecognized color parameter %s" % color) from None
            else:
                return color


def CheckForResize():
    for resize_event in pygame.event.get(VIDEORESIZE):
        return resize_event.size
    return get_surface().get_size()


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
MAX_COLOR = 255


def blend_rgba(color1, color2):
    color1, color2 = toColor(color1), toColor(color2)
    
    r1, g1, b1, a1 = color1
    r2, g2, b2, a2 = color2
    suma = a1 + a2
    if suma > MAX_COLOR:
        a2 -= suma - MAX_COLOR
        suma = MAX_COLOR
    
    r = r1 * a1 / suma + r2 * a2 / suma
    g = g1 * a1 / suma + g2 * a2 / suma
    b = b1 * a1 / suma + b2 * a2 / suma
    a = min(suma, MAX_COLOR)
    
    return Color(round(r), round(g), round(b), a)


pygame_Sprite = pygame.sprite.Sprite
Clock = pygame.time.Clock
clock = Clock()
tick = clock.tick

WHITE  = toColor("white")
BLACK  = toColor("black")
RED    = toColor("red")
BLUE   = toColor("blue")
GREEN  = toColor("green")
ORANGE = toColor("orange")
