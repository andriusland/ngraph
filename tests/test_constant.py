# ----------------------------------------------------------------------------
# Copyright 2016 Nervana Systems Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ----------------------------------------------------------------------------
"""
Test the usage of ng.Constant
"""
from __future__ import print_function

import ngraph as ng
import numpy as np
from ngraph.util.utils import executor


def test_constant_init(transformer_factory):
    """TODO."""
    a = ng.Constant(5)
    result = executor(a)()
    print(result)

    assert (result == 5)
    print("pass constant initialization")

    nparray = np.array(range(5))
    a = ng.Constant(nparray)
    result = executor(a)()
    np.testing.assert_allclose(result, nparray)


def test_constant_add(transformer_factory):
    """TODO."""
    a = ng.Constant(1)
    b = ng.Constant(2)
    c = a + b

    result = executor(c)()
    print(result)
    assert result == 3


def test_constant_multiply(transformer_factory):
    """TODO."""
    a = ng.Constant(4)
    b = ng.Constant(2)
    c = ng.multiply(a, b)
    result = executor(c)()
    assert result == 8


def test_numpytensor_add(transformer_factory):
    """TODO."""
    Y = ng.Axis(name='Y', length=2)
    M = ng.Axis(name='M', length=2)
    N = ng.Axis(name='N', length=2)

    a = ng.Constant(np.array([3, 5], dtype=np.float32), axes=[Y])
    b = ng.Constant(np.array([3, 5], dtype=np.float32), axes=[Y])
    c = a + b
    result = executor(c)()
    assert np.array_equal(result, [6, 10])

    np_a = np.array([[1, 2], [3, 4]], dtype=np.float32)
    np_b = np.array([[1, 2], [3, 4]], dtype=np.float32)
    np_c = np_a + np_b

    a = ng.Constant(np_a, axes=[M, N])
    b = ng.Constant(np_b, axes=[M, N])
    c = a + b
    result = executor(c)()
    assert np.array_equal(result, np_c)


def test_numpytensor_dot(transformer_factory):
    Y = ng.Axis(name='Y')
    M = ng.Axis(name='M')
    N = ng.Axis(name='N')

    np_a = np.array([[1, 2, 3]], dtype=np.float32)
    np_b = np.array([[1, 2], [2, 3], [3, 4]], dtype=np.float32)
    np_c = np.dot(np_a, np_b)

    M.length = 1
    N.length = 3
    a = ng.Constant(np_a, axes=[M, N])
    N.length = 3
    Y.length = 2
    b = ng.Constant(np_b, axes=[N, Y])
    c = ng.dot(a, b)
    result = executor(c)()

    assert np.array_equal(result, np_c)


def test_numpytensor_multiply_constant(transformer_factory):
    """TODO."""
    M = ng.Axis(name='M')
    N = ng.Axis(name='N')

    np_a = np.array([[1, 2, 3]], dtype=np.float32)
    np_c = np.multiply(np_a, 2)

    M.length = 1
    N.length = 3
    a = ng.Constant(np_a, axes=[M, N])
    b = ng.Constant(2)
    c = ng.multiply(a, b)
    result = executor(c)()
    print(result)
    assert np.array_equal(result, np_c)


def test_numpytensor_add_constant(transformer_factory):
    """TODO."""
    M = ng.Axis(name='M')
    N = ng.Axis(name='N')

    np_a = np.array([[1, 2, 3]], dtype=np.float32)
    np_c = np.add(np_a, 2)

    M.length = 1
    N.length = 3
    a = ng.Constant(np_a, axes=[M, N])
    b = ng.Constant(2)
    c = ng.add(a, b)
    result = executor(c)()
    print(result)
    assert np.array_equal(result, np_c)


def test_numpytensor_fusion(transformer_factory):
    """TODO."""
    M = ng.Axis(name='M')
    N = ng.Axis(name='N')

    np_a = np.array([[1, 2, 3]], dtype=np.float32)
    np_b = np.array([[3, 2, 1]], dtype=np.float32)
    np_d = np.multiply(np_b, np.add(np_a, 2))

    M.length = 1
    N.length = 3
    a = ng.Constant(np_a, axes=[M, N])
    b = ng.Constant(np_b, axes=[M, N])
    c = ng.Constant(2)
    d = ng.multiply(b, ng.add(a, c))
    result = executor(d)()
    print(result)
    assert np.array_equal(result, np_d)


def test_numpytensor_mlp(transformer_factory):
    """TODO."""
    D = ng.Axis(name='D')
    H = ng.Axis(name='H')
    N = ng.Axis(name='N')

    np_x = np.array([[1, 2, 3]], dtype=np.float32)
    np_w = np.array([[1, 1], [1, 1], [1, 1]], dtype=np.float32)
    np_b = np.array([1, 2], dtype=np.float32)
    np_c = np.dot(np_x, np_w) + np_b

    N.length = 1
    D.length = 3
    H.length = 2
    x = ng.Constant(np_x, axes=[N, D])
    w = ng.Constant(np_w, axes=[D, H])
    b = ng.Constant(np_b, axes=[H])
    wx = ng.dot(x, w)
    c = wx + b
    result = executor(c)()
    print(result)
    print(np_c)
    assert np.array_equal(result, np_c)