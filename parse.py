"""Functions for parsing various strings to RGB tuples."""

import json
import re
from pathlib import Path

from .basic import hex_to_rgb

__colornames = Path(__file__, "..", "colornames").resolve()
with (__colornames / "css.json").open() as f:
    _css_names = json.load(f)
with (__colornames / "crayola.json").open() as f:
    _crayola_names = json.load(f)
with (__colornames / "xkcd.json").open() as f:
    _xkcd_names = json.load(f)
with (__colornames / "meodai-best.json").open() as f:
    _meodai_best_names = json.load(f)
with (__colornames / "meodai.json").open() as f:
    _meodai_names = json.load(f)
del f


def parse_hex6(hex6):
    """Example: #ab34df"""
    if m := re.match(r"^#?([0-9A-Fa-f]{6})$", hex6.strip()):
        h = int(m.group(1), 16)
        return hex_to_rgb(h)
    raise ValueError(f"String {hex6!r} does not match hex6 format.")


def parse_hex3(hex3):
    """Example: #a3d"""
    if m := re.match(r"^#?([0-9A-Fa-f]{3})$", hex3.strip()):
        h3 = m.group(1)
        return tuple(int(c * 2, 16) for c in h3)
    raise ValueError(f"String {hex3!r} does not match hex3 format.")


def parse_rgbfunc_int(rgbfunc):
    """Example: rgb(171, 52, 223)"""
    if m := re.match(
        r"^rgb\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*\)$", rgbfunc.strip()
    ):
        t = tuple(map(int, m.groups()))
        if not any(n > 255 for n in t):
            return t
    raise ValueError(f"String {rgbfunc!r} does not match rgbfunc_int format.")


def parse_rgbfunc_float(rgbfunc):
    """Example: rgb(0.67, 0.2, 0.87)"""
    if m := re.match(
        r"^rgb\(\s*([01]\.\d+)\s*,\s*([01]\.\d+)\s*,\s*([01]\.\d+)\s*\)$",
        rgbfunc.strip(),
    ):
        t = tuple(map(float, m.groups()))
        if not any(n > 1 for n in t):
            return tuple(int(round(n * 255)) for n in t)
    raise ValueError(f"String {rgbfunc!r} does not match rgbfunc_float format.")


def parse_rgbfunc_percent(rgbfunc):
    """Example: rgb(67%, 20%, 87.5%)"""
    if m := re.match(
        r"^rgb\(\s*(\d{1,3}(?:\.\d+)?)%\s*,\s*(\d{1,3}(?:\.\d+)?)%\s*,\s*(\d{1,3}(?:\.\d+)?)%\s*\)$",
        rgbfunc.strip(),
    ):
        t = tuple(map(float, m.groups()))
        if not any(n > 100 for n in t):
            return tuple(int(round(n * 255 / 100)) for n in t)
    raise ValueError(f"String {rgbfunc!r} does not match rgbfunc_percent format.")


def parse_name_css(name):
    name = name.lower()
    if name not in _css_names:
        raise ValueError(f"Color {name!r} is not named in the CSS dataset.")
    return parse_hex6(_css_names[name])


def parse_name_crayola(name):
    name = name.lower()
    if name not in _crayola_names:
        raise ValueError(f"Color {name!r} is not named in the crayola dataset.")
    return parse_hex6(_crayola_names[name])


def parse_name_xkcd(name):
    name = name.lower()
    if name not in _xkcd_names:
        raise ValueError(f"Color {name!r} is not named in the xkcd dataset.")
    return parse_hex6(_xkcd_names[name])


def parse_name_meodai_best(name):
    name = name.lower()
    if name not in _meodai_best_names:
        raise ValueError(f"Color {name!r} is not named in the meodai-best dataset.")
    return parse_hex6(_meodai_best_names[name])


def parse_name_meodai(name):
    name = name.lower()
    if name not in _meodai_names:
        raise ValueError(f"Color {name!r} is not named in the meodai dataset.")
    return parse_hex6(_meodai_names[name])


def parse(
    colstr,
    *,
    hex6=True,
    hex3=True,
    rgbfunc_int=True,
    rgbfunc_float=True,
    rgbfunc_percent=True,
    name_css=True,
    name_crayola=True,
    name_xkcd=True,
    name_meodai_best=True,
    name_meodai=True,
):
    """Combine all other parse functions into one "universal" function. Use kwargs to disable certain parsers."""
    funcs = []
    if hex6:
        funcs.append(parse_hex6)
    if hex3:
        funcs.append(parse_hex3)
    if rgbfunc_int:
        funcs.append(parse_rgbfunc_int)
    if rgbfunc_float:
        funcs.append(parse_rgbfunc_float)
    if rgbfunc_percent:
        funcs.append(parse_rgbfunc_percent)
    if name_css:
        funcs.append(parse_name_css)
    if name_crayola:
        funcs.append(parse_name_crayola)
    if name_xkcd:
        funcs.append(parse_name_xkcd)
    if name_meodai_best:
        funcs.append(parse_name_meodai_best)
    if name_meodai:
        funcs.append(parse_name_meodai)

    res = None
    for func in funcs:
        try:
            res = func(colstr)
        except ValueError:
            pass
    if res is None:
        raise ValueError(f"Could not find a working parser for {colstr!r}.")
    return res
