import ctypes.wintypes


class Clock:
    @staticmethod
    def get_tick():
        system_time = ctypes.wintypes.FILETIME()
        ctypes.windll.kernel32.GetSystemTimePreciseAsFileTime(ctypes.byref(system_time))
        large = (system_time.dwHighDateTime << 32) + system_time.dwLowDateTime
        return (large // 10 - 11644473600000000) / 1000


def get_center(surface1, surface2):
    w1, h1 = surface1.get_size()
    w2, h2 = surface2.get_size()

    return (w1 - w2) / 2, (h1 - h2) / 2


def hex_to_rgb(h):
    h = h.strip('#')
    if len(h) == 3:
        h = h * 2

    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


class LinearGradient:
    @staticmethod
    def calculate(color1, color2, pos):
        r1, g1, b1 = color1
        r2, g2, b2 = color2

        r = r1 + (r2 - r1) * pos
        g = g1 + (g2 - g1) * pos
        b = b1 + (b2 - b1) * pos

        return (r, g, b)
