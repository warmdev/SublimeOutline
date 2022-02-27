#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sublime
from os.path import basename

ST3 = int(sublime.version()) >= 3000

if ST3:
    from .common import first, set_proper_scheme, calc_width, get_group
else:
    from common import first, set_proper_scheme, calc_width, get_group


def set_active_group(window, view, other_group):
    nag = window.active_group()
    if other_group:
        group = 0 if other_group == 'left' else 1
        groups = window.num_groups()
        if groups == 1:
            width = calc_width(view)
            cols = [0.0, width, 1.0] if other_group == 'left' else [0.0, 1-width, 1.0]
            window.set_layout({"cols": cols, "rows": [0.0, 1.0], "cells": [[0, 0, 1, 1], [1, 0, 2, 1]]})
        elif view:
            group = get_group(groups, nag)
        window.set_view_index(view, group, 0)
    else:
        group = nag

    # when other_group is left, we need move all views to right except FB view
    if nag == 0 and other_group == 'left' and group == 0:
        for v in reversed(window.views_in_group(nag)[1:]):
            window.set_view_index(v, 1, 0)

    return (nag, group)


def set_view(view_id, window, ignore_existing, single_pane):
    view = None
    active_view = None
    if view_id:
        # The Goto command was used so the view is already known and its contents should be
        # replaced with the new path.
        view = first(window.views(), lambda v: v.id() == view_id)

    if not view and not ignore_existing:
        # See if any reusable view exists in case of single_pane argument
        any_path = lambda v: v.score_selector(0, "text.outline") > 0
        view = first(window.views(), any_path if single_pane else same_path)

    if not view:
        active_view = window.active_view()
        view = window.new_file()
        view.set_syntax_file('Packages/Outline/outline.hidden-tmLanguage')
        view.set_scratch(True)
        if view.settings().get('outline_inherit_color_scheme'):
            view.settings().set('color_scheme', active_view.settings().get('color_scheme'))
        else:
            view.settings().add_on_change('color_scheme', lambda: set_proper_scheme(view))
        
        reset_sels = True
    else:
        reset_sels = path != view.settings().get('outline_path', '')

    return (view, reset_sels)


def show(window, view_id=None, ignore_existing=False, single_pane=False, other_group='', layout=1):
    """
    Determines the correct view to use, creating one if necessary, and prepares it.
    """
    symlist = []
    file_path = None
    prev_focus = None
    if other_group:
        prev_focus = window.active_view()
        symlist = prev_focus.get_symbols()
        file_path = prev_focus.file_name()
        # simulate 'toggle sidebar':
        if prev_focus and 'outline' in prev_focus.scope_name(0):
            window.run_command('close_file')
            return

    view, reset_sels = set_view(view_id, window, ignore_existing, single_pane)

    nag, group = set_active_group(window, view, other_group)

    if other_group and prev_focus:
        window.focus_view(prev_focus)

    view_name = "Outline"

    if ST3:
        name = u"𝌆 {0}".format(view_name)
    else:
        name = u"■ {0}".format(view_name)

    view.set_name(name)
    view.settings().set('outline_rename_mode', False)
    window.focus_view(view)

    if layout >= 2:
        window.run_command('dired', {'immediate': True, 'other_group': 'right', 'single_pane': True, 'project': True})

    width = calc_width(view)
    if layout == 0:
        window.set_layout({"cols": [0.0, width, 1-width, 1.0], "rows": [0.0, 0.5, 1.0], "cells": [[2, 0, 3, 2], [0, 0, 2, 2]]})
    elif layout == 1:
        window.set_layout({"cols": [0.0, width, 1-width, 1.0], "rows": [0.0, 0.5, 1.0], "cells": [[0, 0, 1, 2], [1, 0, 3, 2]]})
    elif layout == 2:
        window.set_layout({"cols": [0.0, width, 1-width, 1.0], "rows": [0.0, 0.5, 1.0], "cells": [[2, 0, 3, 2], [1, 0, 2, 2], [0, 0, 1, 2]]})
    elif layout == 3:
        window.set_layout({"cols": [0.0, width, 1-width, 1.0], "rows": [0.0, 0.5, 1.0], "cells": [[0, 1, 1, 2], [1, 0, 3, 2], [0, 0, 1, 1]]})
    elif layout == 4:
        window.set_layout({"cols": [0.0, width, 1-width, 1.0], "rows": [0.0, 0.5, 1.0], "cells": [[2, 1, 3, 2], [0, 0, 2, 2], [2, 0, 3, 1]]})

    window.set_view_index(view, 0, 0)

    for v in reversed(window.views_in_group(0)[1:]):
        if layout >= 2 and u"𝌆" in v.name():
            window.set_view_index(v, 2, 0)
        else:
            window.set_view_index(v, 1, 0)

    window.focus_view(prev_focus)
    
    refresh_sym_view(view, symlist, file_path)

def refresh_sym_view(sym_view, symlist, path):
    l = [symbol for range, symbol in symlist]
    k = [(range.a, range.b) for range, symbol in symlist]
    if sym_view != None:
        sym_view.settings().erase('symlist')
        sym_view.settings().erase('symkeys')
        sym_view.run_command('outline_refresh', {'symlist': l, 'symkeys': k, 'path': path})

def get_sidebar_views_groups(view):
    window = view.window()
    views = window.views()
    sym_view = None
    sym_group = None
    fb_view = None
    fb_group = None
    for v in views:
        if 'outline.hidden-tmLanguage' in v.settings().get('syntax'):
            sym_view = v
            sym_group, i = window.get_view_index(sym_view)
        if u'𝌆' in v.name() and v.id() != sym_view.id():
            fb_view = v
            if fb_view != None:
                fb_group, j = window.get_view_index(fb_view)

    return (sym_view, sym_group, fb_view, fb_group)

def get_sidebar_status(view):
    sidebar_on = False
    for v in view.window().views():
        if u'𝌆' in v.name():
            sidebar_on = True

    return sidebar_on

# given a sorted array, returns the location of x if inserted into the array
def binary_search(array, x):
    low = 0
    high = len(array) - 1
    mid = 0

    while low < high:
        # middle location
        mid = (high + low) // 2
        if array[mid] <= x:
            low = mid + 1
        else:
            high = mid

    return low
