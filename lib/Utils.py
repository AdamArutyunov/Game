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
