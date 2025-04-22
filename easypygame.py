import threading as _threading
try:
    import flat_gui_base as _base, fm as _math, func as _func, iter as _iter
    from fm import RADIANS, DEGREES
except:
    from . import flat_gui_base as _base, fm as _math, func as _func, iter as _iter
    from .fm import RADIANS, DEGREES
from pygame.constants import *
fixed_parameters = _func.fixed_parameters


def rotate_point(a0, a1, angle):
    x1, y1 = a0
    x2, y2 = a1
    
    x = x1 - x2
    y = y1 - y2
    
    x_rotated = x * _math.cos(angle) - y * _math.sin(angle)
    y_rotated = x * _math.sin(angle) + y * _math.cos(angle)
    
    new_x = x_rotated + x2
    new_y = y_rotated + y2
    
    return (new_x, new_y)


FPS = 60


class Sprite(_base.Sprite):
    def __init__(self, shapes):
        self.shapes = shapes
        self.shape_index = 0
        self.shape_size = 1
        self.relative_center = (0.5, 0.5)
        super(Sprite, self).__init__(shapes[0])
    
    def update(self, *args, **kwargs):
        super(Sprite, self).update(*args, **kwargs)
        self.set_image(self.shapes[self.shape_index])
        self.set_image(self.shapes[self.shape_index], (
                self.shape_size * self.width,
                self.shape_size * self.height,
        ))
    
    @property
    def center(self):
        return (self.x + self.relative_center[0] * self.width, self.y + self.relative_center[1] * self.height)
    
    @center.setter
    def center(self, value):
        self.x = value[0] - self.relative_center * self.width
        self.y = value[1] - self.relative_center * self.width
    
    def set_shape(self, index):
        self.shape_index = index
    
    def next_shape(self):
        self.shape_index += 1
    
    @_func.overload
    def angleright(self, angle, center=None):
        if center is None:
            center = self.center
        self.goto(*rotate_point(self.xy, center, angle.radians))
    
    @_func.overload
    def angleright(self, types, number, center=None):
        self.angleleft(self, _math.Angle(types, number), center)
    
    @_func.overload
    def angleleft(self, angle, center=None):
        self.angleright(angle, center)
    
    @_func.overload
    def angleleft(self, types, number, center=None):
        self.angleright(_math.Angle(types, number), center)
    
    def goto(self, x, y):
        self.x = x - self.width * self.relative_center[0]
        self.y = y - self.height * self.relative_center[1]


def complete_within(func, time):
    """
    args and kwargs must (length or angle) /= (time * FPS)
    """
    def to_start():
        for i in range(round(time)):
            func()
            _base.clock.tick(FPS)
    
    time *= FPS
    to_start()


_broadcasts = set()


def make_broadcast(name):
    _broadcasts.add(name)


def receive_broadcast(name):
    return name in _broadcasts


def get_ticks():
    return _base.time.get_ticks()


def get_distance(a0, a1):
    a0 = tuple(a0)
    a1 = tuple(a1)
    return _math.sqrt((a0[0] - a1[0]) ** 2 + (a0[1] - a1[1]) ** 2)


def click(keys=(1,), max_time=500, max_distance=5, rect=None):
    rect: _base.Rect
    click_pos = None
    click_time = None
    for event in check_event(MOUSEBUTTONUP, MOUSEBUTTONDOWN):
        print(event)
        if event.type == MOUSEBUTTONDOWN:
            if event.key in keys:
                click_pos = mouse_position()
                click_time = get_ticks()
        elif click_time is not None:
            print("Check mouse")
            if (
                get_ticks() - click_time <= time and
                get_distance(mouse_position(), click_pos) <= max_distance and
                (rect is None or rect.collidepoint(click_pos))
            ):
                return True
            click_time = None
            click_pos = None


def get_event(func):
    tmp = []
    for event in _base.event.get():
        if func(event):
            tmp.append(event)
        else:
            _base.event.post(event)
    return tmp


def press_key(keys, types):
    for event in get_event(lambda e: e.type in types and e.key in keys):
        if event.key in keys:
            return event
        _base.event.post(event)


def delay(time):
    _base.time.delay(time * 1000)


def mouse_position(x=None):
    if x is None:
        return _base.mouse.get_pos()
    else:
        _base.mouse.set_pos(x)


def check_event(*types):
    tmp = []
    types = _iter.flatten(types)
    for event in get_event(lambda event: event in types):
        tmp.append(event)
    return tmp


def check_basic():
    def check_quit(event):
        return event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE)
    for event in get_event(check_quit):
        quit_game()
        return

    def check_minmize(event):
        return event.type == KEYUP and event.key == K_F10
    for event in get_event(check_minmize):
        _base.iconify()


_running = True
NAME = 0


def start(func, start_factor, times=None, new_thread=True):
    if new_thread and times is None:
        times = 1
    else:
        times = -1
    
    def to_start():
        check_time = times
        while check_time != 0 and _running:
            try:
                if start_factor():
                    func()
                    check_time -= 1
            except _base.error:
                return
    
    if new_thread:
        global NAME
        _threading.Thread(daemon=True, target=to_start, name="start_Thread-%d" % NAME).start()
        NAME += 1
    else:
        to_start()


display_screen = None
screen = None
backgrounds = _base.Backgrounds(_base.Background(None))
quit_command = lambda: None
backgrounds.set_background(backgrounds.backgrounds[0])


def update():
    for bakground in backgrounds:
        bakground: _base.Background
        bakground.surface = screen
    backgrounds.update()
    backgrounds.draw(screen)
    display_screen.blit(screen, (0, 0))
    _base.display.flip()


def start_game():
    global _running, screen, display_screen
    display_screen = _base.set_mode((640, 480), _base.RESIZABLE)
    screen = display_screen.convert_alpha()
    while _running:
        screen.fill((255, 255, 255, 255))
        check_basic()
        if not _running:
            return
        update()
        _base.clock.tick(FPS)


_threading.Thread(target=start_game).start()


def quit_game():
    quit_command()
    global _running
    _running = False
    _base.pygame.quit()


def screen_size(size=None):
    global display_screen, screen
    if size is not None:
        print("resize")
        display_screen = _base.set_mode(size, _base.RESIZABLE)
        print("set_display")
        screen = display_screen.convert_alpha()
        print("set_screen")
        resize_event = _base.event.Event(_base.VIDEORESIZE, {'w': size[0], 'h': size[1]})
        _base.event.post(resize_event)
    else:
        return screen.get_size()
    

if __name__ == "__main__":
    # import time
    # time.sleep(1)
    # print(screen_size())
    # screen_size((1920, 1080))
    # print(screen_size())
    start(lambda: print("Click mouse!"), click, times=-1)
    # time.sleep(3)
    # quit()
    
