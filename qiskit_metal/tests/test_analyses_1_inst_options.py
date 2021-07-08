# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2017, 2021.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

# pylint: disable-msg=unnecessary-pass
# pylint: disable-msg=broad-except
# pylint: disable-msg=import-error
# pylint: disable-msg=too-many-public-methods
"""Qiskit Metal unit tests analyses functionality."""

from pathlib import Path
import unittest

from qiskit_metal.analyses.core.base import QAnalysis
from qiskit_metal.analyses.core.base_with_renderer import QAnalysisRenderer
from qiskit_metal.analyses.quantization.energy_participation_ratio import EPRanalysis
from qiskit_metal.analyses.quantization.lumped_oscillator_model import LOManalysis
from qiskit_metal.analyses.quantization.sim_lumped_elements import LumpedElementsSim
from qiskit_metal.analyses.quantization.sim_eigenmode import EigenmodeSim
from qiskit_metal.analyses.quantization.sim_scattering_impedance import ScatteringImpedanceSim
from qiskit_metal.analyses.hamiltonian.transmon_charge_basis import Hcpb
from qiskit_metal.analyses.sweep_options.sweeping import Sweeping
from qiskit_metal.tests.assertions import AssertionsMixin
from qiskit_metal import designs

TEST_DATA = Path(__file__).parent / "test_data"


class TestAnalyses(unittest.TestCase, AssertionsMixin):
    """Unit test class."""

    def setUp(self):
        """Setup unit test."""
        pass

    def tearDown(self):
        """Tie any loose ends."""
        pass

    def test_analyses_instantiate_hcpb(self):
        """Test instantiation of Hcpb in analytic_transmon.py."""
        try:
            Hcpb()
        except Exception:
            self.fail("Hcpb() failed")

        try:
            Hcpb(nlevels=15)
        except Exception:
            self.fail("Hcpb(nlevels=15) failed")

        try:
            Hcpb(nlevels=15, Ej=13971.3)
        except Exception:
            self.fail("Hcpb(nlevels=15, Ej=13971.3) failed")

        try:
            Hcpb(nlevels=15, Ej=13971.3, Ec=295.2)
        except Exception:
            self.fail("Hcpb(nlevels=15, Ej=13971.3, Ec=295.2) failed")

        try:
            Hcpb(nlevels=15, Ej=13971.3, Ec=295.2, ng=0.001)
        except Exception:
            self.fail("Hcpb(nlevels=15, Ej=13971.3, Ec=295.2, ng=0.001) failed")

    def test_analyses_instantiate_sweeping(self):
        """Test instantiation of Sweeping in analytic_transmon.py."""
        try:
            design = designs.DesignPlanar()
            Sweeping(design)
        except Exception:
            self.fail("Sweeping failed.")

    def test_analyses_instantiate_lumpedelementssim(self):
        """Test instantiation of LumpedElementsSim."""
        design = designs.DesignPlanar()

        try:
            LumpedElementsSim(design)
        except Exception:
            self.fail("LumpedElementsSim failed.")

        try:
            LumpedElementsSim(design, 'capExtractName')
        except Exception:
            self.fail("LumpedElementsSim(design, renderer_name) failed.")

    def test_analyses_instantiate_eigenmodesim(self):
        """Test instantiation of EigenmodeSim."""
        design = designs.DesignPlanar()

        try:
            EigenmodeSim(design)
        except Exception:
            self.fail("EigenmodeSim failed.")

        try:
            EigenmodeSim(design, 'eigenName')
        except Exception:
            self.fail("EigenmodeSim(design, renderer_name) failed.")

    def test_analyses_instantiate_ScatteringImpedanceSim(self):
        """Test instantiation of ScatteringImpedanceSim."""
        design = designs.DesignPlanar()

        try:
            ScatteringImpedanceSim(design)
        except Exception:
            self.fail("ScatteringImpedanceSim failed.")

        try:
            ScatteringImpedanceSim(design, 'impName')
        except Exception:
            self.fail("ScatteringImpedanceSim(design, renderer_name) failed.")

    def test_analyses_instantiate_lomanalysis(self):
        """Test instantiation of LOManalysis."""
        try:
            design = designs.DesignPlanar()
            LOManalysis(design)
        except Exception:
            self.fail("LOManalysis failed.")

    def test_analyses_instantiate_epranalysis(self):
        """Test instantiation of EPRanalysis."""
        try:
            design = designs.DesignPlanar()
            EPRanalysis(design)
        except Exception:
            self.fail("EPRanalysis failed.")

    def test_analyses_qanalysis_default_setup(self):
        """Test that the contents of default_setup in QAnalysis haven't accidentally changed."""
        default_setup = QAnalysis.default_setup
        self.assertEqual(len(default_setup), 0)

    def test_analyses_qanalysisrenderer_default_setup(self):
        """Test that the contents of default_setup in QAnalysisRenderer haven't accidentally
        changed."""
        default_setup = QAnalysisRenderer.default_setup

        self.assertEqual(len(default_setup), 1)
        self.assertEqual(len(default_setup['sim']), 2)
        self.assertEqual(default_setup['sim']['name'], "Setup")
        self.assertEqual(default_setup['sim']['reuse_selected_design'], True)

    def test_analyses_epranalysis_default_setup(self):
        """Test that the contents of default_setup in EPRanalysis haven't accidentally changed."""
        default_setup = EPRanalysis.default_setup

        self.assertEqual(len(default_setup), 1)
        self.assertEqual(len(default_setup['epr']), 5)
        self.assertEqual(len(default_setup['epr']['junctions']), 1)
        self.assertEqual(len(default_setup['epr']['junctions']['jj']), 4)
        self.assertEqual(len(default_setup['epr']['dissipatives']), 1)

        self.assertEqual(default_setup['epr']['junctions']['jj']['Lj_variable'],
                         'Lj')
        self.assertEqual(default_setup['epr']['junctions']['jj']['Cj_variable'],
                         'Cj')
        self.assertEqual(default_setup['epr']['junctions']['jj']['rect'], '')
        self.assertEqual(default_setup['epr']['junctions']['jj']['line'], '')

        self.assertEqual(
            default_setup['epr']['dissipatives']['dielectrics_bulk'], ['main'])

        self.assertEqual(default_setup['epr']['cos_trunc'], 8)
        self.assertEqual(default_setup['epr']['fock_trunc'], 7)
        self.assertEqual(default_setup['epr']['sweep_variable'], 'Lj')

    def test_analyses_lomanalysis_default_setup(self):
        """Test that the contents of default_setup in LOManalysis haven't accidentally changed."""
        default_setup = LOManalysis.default_setup

        self.assertEqual(len(default_setup), 1)
        self.assertEqual(len(default_setup['lom']), 3)
        self.assertEqual(len(default_setup['lom']['junctions']), 2)

        self.assertEqual(default_setup['lom']['junctions']['Lj'], 12)
        self.assertEqual(default_setup['lom']['junctions']['Cj'], 2)
        self.assertEqual(default_setup['lom']['freq_readout'], 7.0)
        self.assertEqual(default_setup['lom']['freq_bus'], [6.0, 6.2])

    def test_analyses_lumpedelementssim_default_setup(self):
        """Test that the contents of default_setup in LumpedElementsSim haven't accidentally change."""
        default_setup = LumpedElementsSim.default_setup

        self.assertEqual(len(default_setup), 1)
        self.assertEqual(len(default_setup['sim']), 11)

        self.assertEqual(default_setup['sim']['freq_ghz'], 5.0)
        self.assertEqual(default_setup['sim']['save_fields'], False)
        self.assertEqual(default_setup['sim']['enabled'], True)
        self.assertEqual(default_setup['sim']['max_passes'], 15)
        self.assertEqual(default_setup['sim']['min_passes'], 2)
        self.assertEqual(default_setup['sim']['min_converged_passes'], 2)
        self.assertEqual(default_setup['sim']['percent_error'], 0.5)
        self.assertEqual(default_setup['sim']['percent_refinement'], 30)
        self.assertEqual(default_setup['sim']['auto_increase_solution_order'],
                         True)
        self.assertEqual(default_setup['sim']['solution_order'], 'High')
        self.assertEqual(default_setup['sim']['solver_type'], 'Iterative')

    def test_analyses_eigenmodesim_default_setup(self):
        """Test that the contents of default_setup in EigenmodeSim haven't accidentally changed."""
        default_setup = EigenmodeSim.default_setup

        self.assertEqual(len(default_setup), 1)
        self.assertEqual(len(default_setup['sim']), 9)
        self.assertEqual(len(default_setup['sim']['vars']), 2)

        self.assertEqual(default_setup['sim']['min_freq_ghz'], 1)
        self.assertEqual(default_setup['sim']['n_modes'], 1)
        self.assertEqual(default_setup['sim']['max_delta_f'], 0.5)
        self.assertEqual(default_setup['sim']['max_passes'], 10)
        self.assertEqual(default_setup['sim']['min_passes'], 1)
        self.assertEqual(default_setup['sim']['min_converged'], 1)
        self.assertEqual(default_setup['sim']['pct_refinement'], 30)
        self.assertEqual(default_setup['sim']['basis_order'], 1)

        self.assertEqual(default_setup['sim']['vars']['Lj'], '10 nH')
        self.assertEqual(default_setup['sim']['vars']['Cj'], '0 fF')

    def test_analyses_ScatteringImpedanceSim_default_setup(self):
        """Test that the contents of default_setup in ScatteringImpedanceSim haven't accidentally
        changed."""
        default_setup = ScatteringImpedanceSim.default_setup

        self.assertEqual(len(default_setup), 1)
        self.assertEqual(len(default_setup['sim']), 9)
        self.assertEqual(len(default_setup['sim']['vars']), 2)
        self.assertEqual(len(default_setup['sim']['sweep_setup']), 7)

        self.assertEqual(default_setup['sim']['freq_ghz'], 5)
        self.assertEqual(default_setup['sim']['max_delta_s'], 0.1)
        self.assertEqual(default_setup['sim']['max_passes'], 10)
        self.assertEqual(default_setup['sim']['min_passes'], 1)
        self.assertEqual(default_setup['sim']['min_converged'], 1)
        self.assertEqual(default_setup['sim']['pct_refinement'], 30)
        self.assertEqual(default_setup['sim']['basis_order'], 1)

        self.assertEqual(default_setup['sim']['vars']['Lj'], '10 nH')
        self.assertEqual(default_setup['sim']['vars']['Cj'], '0 fF')

        self.assertEqual(default_setup['sim']['sweep_setup']['name'], 'Sweep')
        self.assertEqual(default_setup['sim']['sweep_setup']['start_ghz'], 2.0)
        self.assertEqual(default_setup['sim']['sweep_setup']['stop_ghz'], 8.0)
        self.assertEqual(default_setup['sim']['sweep_setup']['count'], 101)
        self.assertEqual(default_setup['sim']['sweep_setup']['step_ghz'], None)
        self.assertEqual(default_setup['sim']['sweep_setup']['type'], 'Fast')
        self.assertEqual(default_setup['sim']['sweep_setup']['save_fields'],
                         False)


if __name__ == '__main__':
    unittest.main(verbosity=2)
