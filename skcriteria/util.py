#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2016-2017, Cabral, Juan; Luczywo, Nadia
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# * Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.

# * Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.

# * Neither the name of the copyright holder nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


# =============================================================================
# FUTURE
# =============================================================================

from __future__ import unicode_literals


# =============================================================================
# DOCS
# =============================================================================

"""Utilities for scikit-criteria

"""


# =============================================================================
# IMPORTS
# =============================================================================

import numpy as np


# =============================================================================
# CONSTANTS
# =============================================================================

MIN = -1

MAX = 1


# =============================================================================
# FUNCTIONS
# =============================================================================

def criteriarr(criteria):
    criteria = np.asarray(criteria)
    if np.setdiff1d(criteria, [MIN, MAX]):
        msg = "Criteria Array only accept '{}' or '{}' Values. Found {}"
        raise ValueError(msg.format(MAX, MIN, criteria))
    return criteria


def is_mtx(mtx, size=None):
    try:
        mtx = np.asarray(mtx)
        a, b = mtx.shape
        if size and (a, b) != size:
            return False
    except:
        return False
    return True


def nearest(array, value, side=None):
    # based on: http://stackoverflow.com/a/2566508
    #           http://stackoverflow.com/a/3230123
    #           http://stackoverflow.com/a/17119267
    if side not in (None, "gt", "lt"):
        msg = "'side' must be None, 'gt' or 'lt'. Found {}".format(side)
        raise ValueError(msg)

    raveled = np.ravel(array)
    cleaned = raveled[~np.isnan(raveled)]

    if side is None:
        idx = np.argmin(np.abs(cleaned-value))

    else:
        masker, decisor = (
            (np.ma.less_equal,  np.argmin)
            if side == "gt" else
            (np.ma.greater_equal, np.argmax))

        diff = cleaned - value
        mask = masker(diff, 0)
        if np.all(mask):
            return None

        masked_diff = np.ma.masked_array(diff, mask)
        idx = decisor(masked_diff)

    return cleaned[idx]


def iter_equal(a, b):
    if isinstance(a, np.ndarray) or isinstance(b, np.ndarray):
        return np.allclose(a, b, equal_nan=True)
    return a == b
