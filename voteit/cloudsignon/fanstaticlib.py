""" Fanstatic lib"""
from fanstatic import Group
from fanstatic import Library
from fanstatic import Resource

from voteit.core.fanstaticlib import voteit_common_js
from voteit.core.fanstaticlib import voteit_main_css


voteit_cso_lib = Library('voteit_cso', '')

voteit_cso_css = Resource(voteit_cso_lib, 'voteit_cso.css', depends=(voteit_main_css,))

voteit_cso = Group((voteit_cso_css,))
