import pandas as pd
import xarray as xr
from monetio.models import cmaq
from monet.util import tools


class getCMAQ():
    def __init__(self, ifn):
        self.CMAQData = self._open_dataset(ifn).sel(z=0)

    def updateLL(self, gridFil):
        '''使用MCIP的LAT及LON替換掉CMAQData中的'''
        grid = xr.open_dataset(gridFil).sel(TSTEP=0, LAY=0)
        tmp = self.CMAQData.update({'latitude': grid.LAT,
                                    'longitude': grid.LON})

    def getCMAQst(self, lat, lon, vars):
        df = pd.DataFrame()
        xx, yy = self.CMAQData.monet.nearest_ij(lat=lat, lon=lon)
        for vv in vars:
            cmd = 'self.CMAQData.' + vv
            tmpData = eval(cmd)
            tmpData = tmpData.sel(x=xx, y=yy).to_dataframe()
            df = pd.concat([df, tmpData], axis=1)
        df.index = df.index + pd.Timedelta(hours=8)  ###UTC -> Local Time
        return df

    def stInfo(self, stFil, st):
        stData = pd.read_csv(stFil, encoding='utf-8-sig', index_col='ch_name')
        st_info = {'st': st, 'stID':stData.loc[st, 'stID'], 'enName':stData.loc[st, 'en_name'], 
                   'lat':stData.loc[st, 'lat'], 'lon':stData.loc[st, 'lon']}       
        return st_info
           

    def getCMAQ2D(self, var):
        cmd = 'self.CMAQData.' + var
        tmpData = eval(cmd)
        return tmpData

    def _open_dataset(self,fname,
                     earth_radius=6370000,
                     convert_to_ppb=True,
                     drop_duplicates=False,
                     **kwargs):
        """Method to open CMAQ IOAPI netcdf files.

        Parameters
        ----------
        fname : string or list
            fname is the path to the file or files.  It will accept hot keys in
            strings as well.
        earth_radius : float
            The earth radius used for the map projection
        convert_to_ppb : boolean
            If true the units of the gas species will be converted to ppbV

        Returns
        -------
        xarray.DataSet


        """
        # open the dataset using xarray
        dset = xr.open_dataset(fname, **kwargs)

        # get the grid information
        grid = cmaq.grid_from_dataset(dset, earth_radius=earth_radius)
        area_def = cmaq.get_ioapi_pyresample_area_def(dset, grid)
        # assign attributes for dataset and all DataArrays
        dset = dset.assign_attrs({'proj4_srs': grid})
        for i in dset.variables:
            dset[i] = dset[i].assign_attrs({'proj4_srs': grid})
            for j in dset[i].attrs:
                dset[i].attrs[j] = dset[i].attrs[j].strip()

        # get the times
        dset = cmaq._get_times(dset, drop_duplicates=drop_duplicates)

        # get the lat lon
        dset = cmaq._get_latlon(dset, area_def)

        # get Predefined mapping tables for observations
        # dset = _predefined_mapping_tables(dset)

        # rename dimensions
        dset = dset.rename({'COL': 'x', 'ROW': 'y', 'LAY': 'z'})
        # convert all gas species to ppbv
        if convert_to_ppb:
            for i in dset.variables:
                if 'units' in dset[i].attrs:
                    if 'ppmV' in dset[i].attrs['units']:
                        dset[i] *= 1000.
                        dset[i].attrs['units'] = 'ppbV'

        # convert 'micrograms to \mu g'
        for i in dset.variables:
            if 'units' in dset[i].attrs:
                if 'micrograms' in dset[i].attrs['units']:
                    dset[i].attrs['units'] = '$\mu g m^{-3}$'

        return dset
