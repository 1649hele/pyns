import threading as _threading
try:
    import flat_gui_base as _base, fm as _math, func as _func
except:
    from . import flat_gui_base as _base, fm as _math, func as _func


def _rotate_point(x1, y1, x2, y2, angle_degrees):
    """
    计算点 (x1,y1) 绕中心点 (x2,y2) 旋转后的坐标
    :param x1, y1: 待旋转点坐标
    :param x2, y2: 旋转中心点坐标
    :param angle_degrees: 旋转角度（度数，顺时针为正）
    :return: (new_x, new_y) 旋转后的坐标
    """
    # 将角度转换为弧度
    theta = _math.radians(angle_degrees)
    
    # 平移至原点
    x = x1 - x2
    y = y1 - y2
    
    # 旋转计算
    x_rotated = x * _math.cos(theta) - y * _math.sin(theta)
    y_rotated = x * _math.sin(theta) + y * _math.cos(theta)
    
    # 平移回原坐标系
    new_x = x_rotated + x2
    new_y = y_rotated + y2
    
    return (new_x, new_y)


FPS = 60


class Sprite(_base.Sprite):
    def __init__(self, shapes):
        self.shapes = shapes
        self.shape_index = 0
        self.shape_size = 1
        self._center = (0.5, 0.5)
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
        return (self.x + self._center * self.width, self.y + self._center * self.height)
    
    @center.setter
    def center(self, value):
        self._center = value
    
    def set_shape(self, index):
        self.shape_index = index
    
    def next_shape(self):
        self.shape_index += 1
    
    @_func.overload
    def angleright(self, angle, center=None):
        if center is None:
            center = self.center
        self.goto(_rotate_point(self.x, self.y, center[0], center[1], angle.degrees))
    
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
        self.x = x - self.width * self._center[0]
        self.y = y - self.height * self._center[1]
    
    def delay(self, func, time, *args, **kwargs):
        """
        args and kwargs must (length or angle) *= (time * FPS)
        """
        def to_start():
            for i in range(time):
                func(*args, **kwargs)
                _base.clock.tick(FPS)
        
        time *= FPS
        _threading.Thread(daemon=True, target=to_start).start()


_broadcasts = set()


def make_broadcast(name):
    _broadcasts.add(name)


def receive_broadcast(name):
    return name in _broadcasts


KEYDOWN = _base.KEYDOWN
KEYUP = _base.KEYUP
MOUSEBUTTONDOWN = _base.MOUSEBUTTONDOWN
MOUSEBUTTONUP = _base.MOUSEBUTTONUP


def press_key(keys, types):
    for event in _base.event.get(types):
        if event.key in keys:
            return event
        _base.event.post(event)


def delay(time):
    _base.time.delay(time / 1000)


def mouse_position(x=None):
    if x is None:
        return _base.mouse.get_pos()
    else:
        _base.mouse.set_pos(x)


def check_mouse(types):
    for event in _base.event.get(types):
        return event


def check_basic():
    for quit_event in _base.event.get((_base.QUIT, KEYUP)):
        if quit_event.type == QUIT or quit_event.key == K_ESCAPE:
            return quit_event
        elif minmize and quit_event.key == minmize:
            return quit_event
        else:
            pygame.event.post(quit_event)


_running = True


def start(func, start_factor, times=None, new_thread=True):
    if new_thread and times is None:
        times = 1
    else:
        times = -1
    
    def to_start():
        check_time = times
        while check_time != 0 and _running:
            if start_factor():
                func()
                check_time -= 1
    
    if new_thread:
        _threading.Thread(daemon=True, target=to_start).start()
    else:
        to_start()


def start_game():
    global _running
    screen = _base.set_mode((640, 480))
    while _running:
        for quit_event in _base.event.get((_base.QUIT, KEYUP)):
            if quit_event.type == _base.QUIT or quit_event.key == _base.K_ESCAPE:
                _running = False
                _base.pygame.quit()
            elif quit_event.key == _base.K_F10:
                _base.iconify()
            else:
                pygame.event.post(quit_event)
        _base.display.flip()


_threading.Thread(target=start_game).start()
    

if __name__ == "__main__":
    start(lambda: print(1), lambda: check_mouse(MOUSEBUTTONUP), new_thread=False)
