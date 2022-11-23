# -*- coding: utf-8 -*-
"""
@author: Elena Volpert
"""
import xarray as xa
import dask
import pandas as pd
import intake
from collections import defaultdict
from dask.diagnostics import progress


def climmean(arr, year1, year2):
    '''calculate climatogical mean'''
    arr.coords['year'] = arr.time.dt.year  # create new coordinate with year
    arr = arr.swap_dims({'time': 'year'}).drop('time')  # remove time coord
    arrmean = arr.sel(year=slice(year1, year2)).mean('year', skipna=True)
    return arrmean


def drop_all_bounds(ds):
    '''substract variables concluding only bonds, example: time_bounds '''
    drop_vars = [vname for vname in ds.coords
                 if (('_bounds') in vname) or ('_bnds') in vname]
    return ds.drop(drop_vars)


def open_dset(df):
    '''open pangeo datasets'''
    # df contains 1 line from catalog_subset
    assert len(df) == 1  # if not, the script raises an AssertionError
    # df.zstore.values:
    # array(['gs://cmip6/CMIP6/ScenarioMIP/AS-RCEC/TaiESM1/ssp585/r1i1p1f1/Amon/tas/gn/v20200901/'],
    # dtype=object)
    # ...[0] - from array in array [[]] to simple array []
    ds = xa.open_zarr(df.zstore.values[0], consolidated=True)
    if not pd.api.types.is_datetime64_ns_dtype(ds['time'].values):
        ds['time'] = ds.indexes['time'].to_datetimeindex()
    return drop_all_bounds(ds)


def open_delayed(df):
    '''lazy operation'''
    return dask.delayed(open_dset)(df)


def download(query, year1, year2):
    '''download CMIP6 model dataset from pangeo datastore'''
    # call pangeo datastore arhive
    catalog = intake.open_esm_datastore(
        "https://storage.googleapis.com/cmip6/pangeo-cmip6.json")

    catalog_subset = catalog.search(require_all_on='source_id', **query)

    dsets = defaultdict(dict)

    for group, df in catalog_subset.df.groupby(by=['source_id',
                                                   'experiment_id']):
        dsets[group[0]][group[1]] = open_delayed(df)

    dsets_ = dask.compute(dict(dsets))[0]

    model_merged = []
    for key, item in dsets_.items():
        # key - sourch_id = model
        # item - array
        model = xa.concat(item.values(), join='outer', dim='time')
        model = model.expand_dims({'model': [key]})
        climatmodel = climmean(model, year1, year2)
        model_merged.append(climatmodel)

    with progress.ProgressBar():
        model_merged_ = dask.compute(model_merged)[0]

    return xa.concat(model_merged_, dim='model', coords='minimal')
