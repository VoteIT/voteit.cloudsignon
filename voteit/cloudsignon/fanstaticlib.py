""" Fanstatic lib"""
from fanstatic import Library
from fanstatic import Resource

from voteit.core.fanstaticlib import voteit_main_css


voteit_cso_lib = Library('voteit_cso', 'static')

voteit_cso = Resource(voteit_cso_lib, 'voteit_cso.css', depends=(voteit_main_css,))
