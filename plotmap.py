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
