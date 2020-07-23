#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# MIT License
# Copyright (c) 2020 Stɑrry Shivɑm // This file is part of AcuteBot
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.



from acutebot import LOG
from os.path import dirname, basename, isfile
import glob

def list_modules():
    mod_paths = glob.glob(dirname(__file__) + "/*.py")
    all_modules = [basename(f)[:-3] for f in mod_paths if isfile(f)
                   and f.endswith(".py")
                   and not f.endswith('__init__.py')]
    return all_modules

ALL_FUNCS = sorted(list_modules())
LOG.info("Modules loaded: %s", str(ALL_FUNCS))
__all__ = ALL_FUNCS + ["ALL_FUNCS"]
