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

from typing import Union

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from pyEPR.reports import (plot_convergence_f_vspass, plot_convergence_max_df,
                           plot_convergence_maxdf_vs_sol,
                           plot_convergence_solved_elem)

from ... import Dict
from ..core import QAnalysisRenderer


class EigenmodeSim(QAnalysisRenderer):
    """Compute eigenmode, then derive from it using the epr method

    Default Setup:
        name (str): Name of eigenmode setup. Defaults to "Setup".
        min_freq_ghz (int): Minimum frequency in GHz. Defaults to 1.
        max_delta_f (float): Absolute value of maximum difference in
            frequency. Defaults to 0.5.
        max_passes (int): Maximum number of passes. Defaults to 10.
        min_passes (int): Minimum number of passes. Defaults to 1.
        min_converged (int): Minimum number of converged passes. Defaults to 1.
        pct_refinement (int): Percent refinement. Defaults to 30.
        basis_order (int): Basis order. Defaults to 1.
        vars (Dict): Variables (key) and values (value) to define in the renderer.
    """
    default_setup = Dict(sim=Dict(name="Setup",
                                  min_freq_ghz=1,
                                  n_modes=1,
                                  max_delta_f=0.5,
                                  max_passes=10,
                                  min_passes=1,
                                  min_converged=1,
                                  pct_refinement=30,
                                  basis_order=1,
                                  vars=Dict(Lj='10 nH', Cj='0 fF')))
    """Default setup"""

    def __init__(self, design: 'QDesign', renderer_name: str = 'hfss'):
        """Compute eigenmode, then derive from it using the epr method

        Args:
            design (QDesign): pointer to the main qiskit-metal design. Used to access the Qrenderer
            renderer_name (str, optional): which renderer to use. Defaults to 'hfss'.
        """
        # set design and renderer
        super().__init__(design, renderer_name)

        # settings variables
        self.setup_name = None

        # output variables
        self._convergence_t = None
        self._convergence_f = None

    def _render(self, **design_selection):
        """Renders the design from qiskit metal into the selected renderer.
        First it decides the tentative name of the design. Then it runs the renderer method
        that executes the design rendering. It returns the final design name.

        Returns:
            str: Final design name that the renderer used.
        """
        base_name = self.design.name
        if "name" in design_selection:
            if design_selection["name"] is not None:
                base_name = design_selection["name"]
                del design_selection["name"]
        design_name = base_name + "_" + self.renderer_name
        design_name = self.renderer.execute_design(design_name,
                                                   solution_type='eigenmode',
                                                   **design_selection)
        return design_name

    def _analyze(self):
        """Executes the analysis step of the Run. First it initializes the renderer setup
        to prepare for eignemode analysis, then it executes it. Finally it recovers the
        output of the analysis and stores it in self.convergence_t and self.convergence_f.
        """
        self.setup_name = self.renderer.initialize_eigenmode(**self.setup.sim)

        self.renderer.analyze_setup(self.setup_name)
        self.convergence_t, self.convergence_f = self.renderer.get_convergences(
        )

    def run_sim(self,
                name: str = None,
                components: Union[list, None] = None,
                open_terminations: Union[list, None] = None,
                port_list: Union[list, None] = None,
                jj_to_port: Union[list, None] = None,
                ignored_jjs: Union[list, None] = None,
                box_plus_buffer: bool = True) -> (str, str):
        """Executes the entire eigenmode analysis and convergence result export.
        First it makes sure the tool is running. Then it does what's necessary to render the design.
        Finally it runs the setup defined in this class. So you need to modify the setup ahead.
        You can modify the setup by using the methods defined in the QAnalysis super-class.
        After this method concludes you can inspect the output using this class properties.

        Args:
            name (str): reference name for the somponents selection. If None,
                it will use the design.name. Defaults to None.
            components (Union[list, None], optional): List of components to render.
                Defaults to None.
            open_terminations (Union[list, None], optional):
                List of tuples of pins that are open. Defaults to None.
            port_list (Union[list, None], optional): List of tuples of pins to be rendered as ports.
                Defaults to None.
            jj_to_port (Union[list, None], optional): List of tuples of jj's to be rendered as
                ports. Defaults to None.
            ignored_jjs (Union[list, None], optional): List of tuples of jj's that shouldn't be
                rendered. Defaults to None.
            box_plus_buffer (bool, optional): Either calculate a bounding box based on the location
                of rendered geometries or use chip size from design class. Defaults to True.

        Returns:
            (str, str): Name of the design and name of the setup
        """
        if not self.renderer_initialized:
            self._initialize_renderer()

        renderer_design_name = self._render(name=name,
                                            selection=components,
                                            open_pins=open_terminations,
                                            port_list=port_list,
                                            jj_to_port=jj_to_port,
                                            ignored_jjs=ignored_jjs,
                                            box_plus_buffer=box_plus_buffer)

        self._analyze()
        return renderer_design_name, self.setup_name

    @property
    def convergence_f(self):
        """Convergence of the eigenmode frequency.

        Returns:
            pd.DataFrame: Convergence of the eigenmode frequency.
        """
        return self._convergence_f

    @convergence_f.setter
    def convergence_f(self, conv: pd.DataFrame):
        """Sets the convergence of the eigenmode frequency.

        Args:
            conv (pd.DataFrame): Convergence of the eigenmode frequency.
        """
        self._convergence_f = conv

    @property
    def convergence_t(self):
        """Convergence of the eigenmode frequency.

        Returns:
            pd.DataFrame: Convergence of the eigenmode frequency.
        """
        return self._convergence_t

    @convergence_t.setter
    def convergence_t(self, conv: pd.DataFrame):
        """Sets the convergence of the eigenmode frequency.

        Args:
            conv (pd.DataFrame): Convergence of the eigenmode frequency.
        """
        self._convergence_t = conv

    def recompute_convergences(self, variation: str = None):
        """convergence plots are computed as part of run(). However, in special cases
        you might need to recalculate them using a different variation.

        Args:
            variation (str, optional):  Information from pyEPR; variation should be in the form
            variation = "scale_factor='1.2001'". Defaults to None.
        """
        self.convergence_t, self.convergence_f = self.renderer.get_convergences(
            variation)

    def plot_convergences(self,
                          convergence_t: pd.DataFrame = None,
                          convergence_f: pd.DataFrame = None,
                          fig: mpl.figure.Figure = None,
                          _display: bool = True):
        """Creates 3 plots, useful to determin the convergence achieved by the renderer:
        * convergence frequency vs. pass number if fig is None.
        * delta frequency and solved elements vs. pass number.
        * delta frequency vs. solved elements.

        Args:
            convergence_t (pd.DataFrame): Convergence vs pass number of the eigenemode freqs.
            convergence_f (pd.DataFrame): Convergence vs pass number of the eigenemode freqs.
            fig (matplotlib.figure.Figure, optional): A mpl figure. Defaults to None.
            _display (bool, optional): Display the plot? Defaults to True.
        """

        if convergence_t is None:
            convergence_t = self.convergence_t
        if convergence_f is None:
            convergence_f = self.convergence_f

        if fig is None:
            fig = plt.figure(figsize=(11, 3.))

            # Grid spec and axes;    height_ratios=[4, 1], wspace=0.5
            gs = mpl.gridspec.GridSpec(1, 3, width_ratios=[1.2, 1.5, 1])
            axs = [fig.add_subplot(gs[i]) for i in range(3)]

            ax0t = axs[1].twinx()
            plot_convergence_f_vspass(axs[0], convergence_f)
            plot_convergence_max_df(axs[1], convergence_t.iloc[:, 1])
            plot_convergence_solved_elem(ax0t, convergence_t.iloc[:, 0])
            plot_convergence_maxdf_vs_sol(axs[2], convergence_t.iloc[:, 1],
                                          convergence_t.iloc[:, 0])

            fig.tight_layout(w_pad=0.1)  # pad=0.0, w_pad=0.1, h_pad=1.0)

            # if _display:
            #     from IPython.display import display
            #     display(fig)

    ##### Below methods are related to EPR

    def plot_fields(self, object_name, eigenmode=1, *args, **kwargs):
        """Plots electro(magnetic) fields in the renderer.
        Accepts as args everything parameter accepted by the homonymous renderer method.

        Args:
            object_name (str): Used to plot on faces of.
            eigenmode (int, optional): ID of the mode you intend to plot. Defaults to 1.

        Returns:
            None
        """
        self.renderer.set_mode(eigenmode, self.setup_name)
        return self.renderer.plot_fields(*args,
                                         **kwargs,
                                         object_name=object_name)

    def clear_fields(self, names: list = None):
        """
        Delete field plots from renderer.

        Args:
            names (list, optional): Names of field plots to delete. Defaults to None.
        """
        return self.renderer.clear_fields(names)