import re

import win32gui


class Set_Foregound(object):
    def window_enum_handler(self, hwnd, resultList):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) != '':
            resultList.append((hwnd, win32gui.GetWindowText(hwnd)))

    def get_app_list(self, program, handles=[]) -> int:
        win32gui.EnumWindows(self.window_enum_handler, handles)
        for handle in handles:
            pattern = re.compile(program)
            if pattern.match(handle[1]):
                return handle[0]
        return 0

    def set_foreground(self, program) -> bool:
        """put the window in the foreground"""
        try:
            win32gui.SetForegroundWindow(self.get_app_list(program))
            return True
        except win32gui.error:
            return False


if __name__ == '__main__':
    Set_Foregound().set_foreground("(Discord|.+? - Discord)")
