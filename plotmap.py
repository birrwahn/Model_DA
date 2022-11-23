# -*- coding: utf-8 -*-
"""
@author: Elena Volpert
"""
import matplotlib.pyplot as plt
import numpy as np
import cartopy as cpy
import xarray as xr
from matplotlib.ticker import FormatStrFormatter


def plot_map(ds, ax=None, formatting=True, fs=15,
             lon='lon', lat='lat', title=None,
             cmap='Spectral_r', fr='%.0f',
             extent=None,
             colorlevels=10, extend='both', orientation='vertical',
             colormax=None, colormin=None,
             coastlines=True, grid=True):
        """Plot 2D field with lon-lat grid.

        Call signature::

            plot_map(ds, **kwargs)

            use contourf function from matplotlib.pyplot.
            Could be used for subplots plot due to ax argument.

        Parameters
        ----------
        ds : 2D xarray.DataArray
        The values over which the contour is drawn.

        *ds* must be 2D array with lon-lat coordinates.
        The structure of *ds*:
            ds.coords:
                    lat - 1D array with ``len(lat) == N``, float
                    lon - 1D array with ``len(lon) == M``, flot
                    ds.values -  (N,M) array

        Returns
        -------
        `~.contourf(ds.lon, ds.lat, ds.values)`

        Other Parameters
        ----------------
        ax : a single `~matplotlib.axes.Axes` object, default: None
            Could be used to plot with `~plt.subplots`.

            If not specified:
            ax = plt.axes(projection = cartopy.crs.PlateCarree())

        lat : str, default: 'lat'
            Set the name of the latitude coordinate if is not equal 'lat'.

            Example::
                    lat = 'latitude'

        lon : str, default: 'lon'
            Set the name of the longitude coordinate if is not equal 'lon'.

            Example::
                    lon = 'longitude'

        title : str, default: None
            Set the title of the plot.

        # FORMATTING & MAPPING

        formatting : bool, default: True.
            Format plot with:
                font = {'sans-serif':'Montserrat', 'size': fs}
                axes = {'spines.top':False, 'spines.right':False}
                plt.rc('font',**font)
                plt.rc('axes',**axes)
                plt.rc('lines', linewidth = 1)

            with

        fs : int, default: 15
            It is a fontsize for formatting parameters.

        fr : str, default: %.0f
            Format for colorbar ticks.

        costlines : bolt, default: True
            If ``True`` add costlines with `~.costlines()`.

        grid : bolt, default: True
            If ``True`` add grid with `~.gridlines()`.

        extent : array-like, default: None
            If mapping subregion, format: [lon1, lon2, lat1, lat2]

        # COLORMAP & COLORBAR

        cmap : str or `.Colormap`, default: 'Spectral_r'
            A `.Colormap` instance or registered colormap name.
            !!! `~.contourf()` parameter

         extend : {'neither', 'both', 'min', 'max'}, default: 'both'
            Determines the coloring of values that are outside
            the *colorlevels* range.
            !!! `~.contourf()` parameter

            If 'neither', values outside the *levels* range are not colored.
            If 'min', 'max' or 'both', color the values below, above or below
            and above the *levels* range.

        orientation : None or {'vertical', 'horizontal'}, default: 'vertical'
            The orientation of the colorbar.
            !!! `~.colorbar()` parameter

        colormin, colormax, colorlevels : float,
                                             default:
                                                 colormin = ds.values.min()
                                                 colormax = ds.values.max()
                                                 colorlevels = 10
            Parameters for `~.contourf(levels=np.linspace(colormin,
                                                          colormax,
                                                          colorlevels))`

            Determines the number and positions of the contour regions.

        Notes
        -----
        Required libraries:
                            import matplotlib.pyplot as plt
                            import numpy as np
                            import cartopy as cpy
                            import xarray as xr
                            from matplotlib.ticker import FormatStrFormatter
    """

    assert isinstance(ds, xr.DataArray)
    assert lon in ds.coords
    assert lat in ds.coords

    if formatting:
        font = {'sans-serif': 'Montserrat', 'size': fs}
        axes = {'spines.top': False, 'spines.right': False}
        plt.rc('font', **font)
        plt.rc('axes', **axes)
        plt.rc('lines', linewidth=1)

    if ax is None:
        ax = plt.axes(projection=cpy.crs.PlateCarree())

    if colormax is None:
        colormax = ds.values.max()
        colormin = ds.values.min()

    maps = ax.contourf(ds[lon], ds[lat], ds.values,
                       levels=np.linspace(colormin, colormax, colorlevels),
                       transform=cpy.crs.PlateCarree(),
                       cmap=cmap,
                       extend=extend)

    cax = plt.colorbar(maps, ax=ax, shrink=0.7,
                       orientation=orientation,
                       format=FormatStrFormatter(fr))

    if coastlines:
        ax.coastlines()

    if grid:
        gl = ax.gridlines(draw_labels=True,
                          linewidth=0.5, linestyle='--', color='k')
        gl.xformatter = cpy.mpl.gridliner.LONGITUDE_FORMATTER
        gl.yformatter = cpy.mpl.gridliner.LATITUDE_FORMATTER
        gl.xlabels_top = False
        gl.ylabels_right = False

    if extent is not None:
        ax.set_extent(extent, crs=cpy.crs.PlateCarree())
    else:
        ax.set_global()

    ax.set_title(title)

    return ax, cax
