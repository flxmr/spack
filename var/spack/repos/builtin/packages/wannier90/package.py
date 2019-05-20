# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import inspect
import os.path

from spack import *


class Wannier90(MakefilePackage):
    """Wannier90 calculates maximally-localised Wannier functions (MLWFs).

    Wannier90 is released under the GNU General Public License.
    """
    homepage = 'http://wannier.org'
    url = 'https://github.com/wannier-developers/wannier90/archive/v3.0.0.tar.gz'

    version('3.0.0', sha256='f196e441dcd7b67159a1d09d2d7de2893b011a9f03aab6b30c4703ecbf20fe5b')
    version('2.1.0', sha256='c0e238be22c7d9bf3c93b2651747c75705e97db63173064e679f3820dc85fda4')
    version('2.0.1', '4edd742506eaba93317249d33261fb22')

    depends_on('mpi')
    depends_on('lapack')
    depends_on('blas')

    parallel = False

    build_targets = [
        'wannier', 'post', 'lib', 'w90chk2chk', 'w90vdw', 'w90pov'
    ]

    @property
    def makefile_name(self):
        # Older versions use 'make.sys'
        filename = 'make.sys'

        # While newer search for 'make.inc'
        if self.spec.satisfies('@2.1.0:'):
            filename = 'make.inc'

        abspath = join_path(self.stage.source_path, filename)
        return abspath

    def edit(self, spec, prefix):

        lapack = self.spec['lapack'].libs
        blas = self.spec['blas'].libs
        substitutions = {
            '@F90': spack_fc,
            '@MPIF90': self.spec['mpi'].mpifc,
            '@LIBS': (lapack + blas).joined()
        }

        template = join_path(
            os.path.dirname(inspect.getmodule(self).__file__),
            'make.sys'
        )

        copy(template, self.makefile_name)
        for key, value in substitutions.items():
            filter_file(key, value, self.makefile_name)

    def install(self, spec, prefix):

        mkdirp(self.prefix.bin)
        mkdirp(self.prefix.lib)

        install(
            join_path(self.stage.source_path, 'wannier90.x'),
            join_path(self.prefix.bin, 'wannier90.x')
        )

        install(
            join_path(self.stage.source_path, 'postw90.x'),
            join_path(self.prefix.bin, 'postw90.x')
        )

        install(
            join_path(self.stage.source_path, 'libwannier.a'),
            join_path(self.prefix.lib, 'libwannier.a')
        )

        install(
            join_path(self.stage.source_path, 'w90chk2chk.x'),
            join_path(self.prefix.bin, 'w90chk2chk.x')
        )

        install(
            join_path(self.stage.source_path, 'utility', 'w90vdw', 'w90vdw.x'),
            join_path(self.prefix.bin, 'w90vdw.x')
        )

        install(
            join_path(self.stage.source_path, 'utility', 'w90pov', 'w90pov'),
            join_path(self.prefix.bin, 'w90pov')
        )

        install_tree(
            join_path(self.stage.source_path, 'pseudo'),
            join_path(self.prefix.bin, 'pseudo')
        )
