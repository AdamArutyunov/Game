import ctypes.wintypes


class Clock:
    @staticmethod
    def get_tick():
        system_time = ctypes.wintypes.FILETIME()
        ctypes.windll.kernel32.GetSystemTimePreciseAsFileTime(ctypes.byref(system_time))
        large = (system_time.dwHighDateTime << 32) + system_time.dwLowDateTime
        return (large // 10 - 11644473600000000) / 1000
