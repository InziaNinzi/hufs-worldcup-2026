import pygame

GAME_W = 1000
GAME_H = 600

_state = {
    "real_screen": None,
    "game_surface": None,
    "scale": 1.0,
    "offset_x": 0,
    "offset_y": 0,
    "is_fullscreen": False,
    "orig_flip": None,
}


def _update_layout(rw, rh):
    scale = min(rw / GAME_W, rh / GAME_H)
    sw = int(GAME_W * scale)
    sh = int(GAME_H * scale)
    _state["scale"] = scale
    _state["offset_x"] = (rw - sw) // 2
    _state["offset_y"] = (rh - sh) // 2


def _patched_flip():
    s = _state["scale"]
    ox = _state["offset_x"]
    oy = _state["offset_y"]
    sw = int(GAME_W * s)
    sh = int(GAME_H * s)
    real = _state["real_screen"]
    real.fill((0, 0, 0))
    dest = real.subsurface(pygame.Rect(ox, oy, sw, sh))
    pygame.transform.scale(_state["game_surface"], (sw, sh), dest)
    _state["orig_flip"]()


def init():
    """pygame.init() 이후 호출. 모든 모듈에 넘길 game_surface 반환."""
    _state["game_surface"] = pygame.Surface((GAME_W, GAME_H))
    _state["orig_flip"] = pygame.display.flip
    pygame.display.flip = _patched_flip
    return _state["game_surface"]


def open_windowed():
    """창모드로 열기. 화면 크기의 85% 비율로 자동 계산."""
    info = pygame.display.Info()
    scale = min(info.current_w * 0.85 / GAME_W, info.current_h * 0.85 / GAME_H)
    win_w = int(GAME_W * scale)
    win_h = int(GAME_H * scale)
    real = pygame.display.set_mode((win_w, win_h))
    _state["real_screen"] = real
    _state["is_fullscreen"] = False
    _update_layout(win_w, win_h)
    return real


def open_fullscreen():
    """전체화면으로 열기."""
    real = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    _state["real_screen"] = real
    _state["is_fullscreen"] = True
    _update_layout(*real.get_size())
    return real


def toggle_fullscreen():
    """전체화면 ↔ 창모드 토글."""
    if _state["is_fullscreen"]:
        return open_windowed()
    return open_fullscreen()


def is_fullscreen():
    return _state["is_fullscreen"]


def scale_mouse(pos):
    """마우스 실좌표 → 게임 논리 좌표 변환."""
    s = _state["scale"]
    if s == 0:
        return pos
    ox = _state["offset_x"]
    oy = _state["offset_y"]
    return (int((pos[0] - ox) / s), int((pos[1] - oy) / s))
