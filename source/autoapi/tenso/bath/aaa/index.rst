tenso.bath.aaa
==============

.. py:module:: tenso.bath.aaa

.. autoapi-nested-parse::

   A Python implementation of the AAA algorithm for rational approximation.

   For more information, see the paper

     The AAA Algorithm for Rational Approximation
     Yuji Nakatsukasa, Olivier Sete, and Lloyd N. Trefethen
     SIAM Journal on Scientific Computing 2018 40:3, A1494-A1522

   as well as the Chebfun package <http://www.chebfun.org>. This code is an almost
   direct port of the Chebfun implementation of aaa to Python.

   From https://github.com/c-f-h/aaa/blob/master/aaa.py (BSD 2-Clause License)
   Copyright (c) 2019, Clemens Hofreither
   All rights reserved.

   Redistribution and use in source and binary forms, with or without
   modification, are permitted provided that the following conditions are met:

   1. Redistributions of source code must retain the above copyright notice, this
      list of conditions and the following disclaimer.
   2. Redistributions in binary form must reproduce the above copyright notice,
      this list of conditions and the following disclaimer in the documentation
      and/or other materials provided with the distribution.

   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
   ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
   WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
   DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
   ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
   (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
   LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
   ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
   (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
   SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.



Classes
-------

.. autoapisummary::

   tenso.bath.aaa.BarycentricRational


Functions
---------

.. autoapisummary::

   tenso.bath.aaa.aaa
   tenso.bath.aaa.interpolate_poly
   tenso.bath.aaa.interpolate_with_poles
   tenso.bath.aaa.floater_hormann


Module Contents
---------------

.. py:class:: BarycentricRational(z, f, w)

   A class representing a rational function in barycentric representation.



   .. py:attribute:: nodes


   .. py:attribute:: values


   .. py:attribute:: weights


   .. py:method:: __call__(x)

      Evaluate rational function at all points of `x`



   .. py:method:: polres()

      Return the poles and residues of the rational function.



   .. py:method:: zeros()

      Return the zeros of the rational function.



.. py:function:: aaa(F, Z, tol=1e-13, mmax=100, return_errors=False)

   Compute a rational approximation of `F` over the points `Z`.

   The nodes `Z` should be given as an array.

   `F` can be given as a function or as an array of function values over `Z`.

   Returns a `BarycentricRational` instance which can be called to evaluate
   the rational function, and can be queried for the poles, residues, and
   zeros of the function.


.. py:function:: interpolate_poly(values, nodes)

   Compute the interpolating polynomial for the given nodes and values in
   barycentric form.


.. py:function:: interpolate_with_poles(values, nodes, poles)

   Compute a rational function which interpolates the given values at the
   given nodes and which has the given poles.


.. py:function:: floater_hormann(values, nodes, blending)

   Compute the Floater-Hormann rational interpolant for the given nodes and
   values. See (Floater, Hormann 2007), DOI 10.1007/s00211-007-0093-y.

   The blending parameter (usually called `d` in the literature) is an integer
   between 0 and n (inclusive), where n+1 is the number of interpolation
   nodes. For functions with higher smoothness, the blending parameter may be
   chosen higher. For d=n, the result is the polynomial interpolant.

   Returns an instance of `BarycentricRational`.


