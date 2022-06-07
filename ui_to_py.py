# -*- coding: utf-8 -*-
"""
Created on Tue May 18 10:12:32 2021

@author: Admin
"""

from PyQt5 import uic

   
with open('kampKaydiUI.py', 'w', encoding="utf-8") as fout:
    uic.compileUi('kampKaydi.ui', fout)