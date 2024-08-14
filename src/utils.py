import logging
from logging.config import dictConfig

import time
import os, sys
from datetime import datetime
from netCDF4 import Dataset
import numpy as np

import glob

#####################################################################################################
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx, array[idx]


#####################################################################################################
def get_abi_data(
    dt,
    ch,
    datadir_patt,
    startY=None,
    endY=None,
    startX=None,
    endX=None,
    metadata={},
    return_proj_info=False,
):

    # returns the 2D reflectance or BT array
    try:
        datafile = glob.glob(dt.strftime(f"{datadir_patt}/*C{ch}_*_s%Y%j%H%M%S*.nc"))[0]
    except IndexError:
        try:
            datafile = glob.glob(dt.strftime(f"{datadir_patt}/*C{ch}_*_s%Y%j%H%M*.nc"))[
                0
            ]
        except IndexError:
            logging.error(
                f"Could not get "
                + dt.strftime(f"{datadir_patt}/*C{ch}_*_s%Y%j%H%M%S*.nc")
            )
            raise

    localfile = datafile
    nc = Dataset(localfile, "r")
    metadata["goes_position"] = nc.orbital_slot
    metadata["scene_id"] = nc.scene_id
    metadata["platform_ID"] = nc.platform_ID

    if ch == "02":
        # convert vis radiance to reflectance; crop if necessary
        if startY:
            radiance = nc.variables["Rad"][startY * 4 : endY * 4, startX * 4 : endX * 4]
        else:
            radiance = nc.variables["Rad"][:]
        result = radiance * nc.variables["kappa0"][:]
    elif ch in ["01", "03", "05"]:
        # convert vis radiance to reflectance; crop if necessary
        if startY:
            radiance = nc.variables["Rad"][startY * 2 : endY * 2, startX * 2 : endX * 2]
        else:
            radiance = nc.variables["Rad"][:]
        result = radiance * nc.variables["kappa0"][:]
    elif ch == "04" or ch == "06":
        # convert vis radiance to reflectance; crop if necessary
        if startY:
            radiance = nc.variables["Rad"][startY:endY, startX:endX]
        else:
            radiance = nc.variables["Rad"][:]
        result = radiance * nc.variables["kappa0"][:]
    else:  # IR channels
        # convert IR radiance to BT; crop if necessary
        if startY:
            radiance = nc.variables["Rad"][startY:endY, startX:endX]
        else:
            radiance = nc.variables["Rad"][:]
        result = (
            nc.variables["planck_fk2"][:]
            / (np.log((nc.variables["planck_fk1"][:] / radiance) + 1))
            - nc.variables["planck_bc1"][:]
        ) / nc.variables["planck_bc2"][:]

    if return_proj_info:
        satheight = nc.variables["goes_imager_projection"].getncattr(
            "perspective_point_height"
        )
        x = nc.variables["x"][:] * satheight
        y = nc.variables["y"][:] * satheight

    try:
        nc.close()
    except RuntimeError:
        pass

    # shutil.rmtree(tmpdir, ignore_errors=False) #remove tmpdir

    if return_proj_info:
        return x, y, result
    else:
        return result


####################################################################################################
def read_netcdf(file, datasets, global_atts=None):
    logging.info("Process started. Received " + file)
    # datasets is a dict, formatted thusly:
    # datasets = {'varname1':{'atts':['attname1','attname2']}, 'varname2':{'atts':[]}}
    # atts are variable attributes. If 'atts':['ALL'], then it will grab all variable attributes.
    # global_atts are file global attributes.
    # Each key/var in datasets is returned with a 'data' key...which contains a numpy array

    if file[-3:] == ".gz":
        gzip = 1
        unzipped_file = file[0 : len(file) - 3]
        the_file = unzipped_file
        s = call(["gunzip", "-f", file])
    else:
        gzip = 0
        the_file = file

    try:
        openFile = Dataset(the_file, "r")
    except (OSError, IOError) as err:
        raise

    for key in datasets:
        datasets[key]["data"] = openFile.variables[key][:]
        # get each variable attribute
        if datasets[key]["atts"] == ["ALL"]:
            datasets[key]["atts"] = {}
            for att in openFile.variables[key].ncattrs():
                datasets[key]["atts"][att] = getattr(openFile.variables[key], att)
        # get select variable attributes
        else:
            tmpdict = {}
            for att in datasets[key]["atts"]:
                if att in openFile.variables[key].ncattrs():
                    tmpdict[att] = getattr(openFile.variables[key], att)
            datasets[key]["atts"] = tmpdict
    # get global attributes
    if isinstance(global_atts, dict):
        if 'ALL' in global_atts:
            del global_atts['ALL']
            for gatt in openFile.ncattrs():
                global_atts[gatt] = getattr(
                    openFile, gatt
                )
        else:
            for gatt in global_atts:
                if gatt in openFile.ncattrs():
                    global_atts[gatt] = getattr(
                        openFile, gatt
                    )  # global_atts is modified and returned
    openFile.close()

    # --gzip file after closing?
    if gzip:
        # s = Popen(['gzip','-f',unzipped_file]) #==will run in background since it doesn't need output from command.
        s = call(["gzip", "-f", unzipped_file])

    logging.info("Process ended.")


#####################################################################################################
def write_netcdf(
    output_file, datasets, dims, atts={}, gzip=False, wait=False, nc4=False, **kwargs
):
    logging.info("Process started")


    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    if nc4:
        ncfile = Dataset(output_file, "w")
    else:
        ncfile = Dataset(output_file, "w" ,format='NETCDF3_CLASSIC')

    # dimensions
    for dim in dims:
        ncfile.createDimension(dim, dims[dim])
    # variables
    for varname in datasets:
        try:
            dtype = datasets[varname]["data"].dtype.str
        except AttributeError:
            if isinstance(datasets[varname]["data"], int):
                dtype = "int"
            elif isinstance(datasets[varname]["data"], float):
                dtype = "float"

        if "_FillValue" in datasets[varname]["atts"]:
            dat = ncfile.createVariable(
                varname,
                dtype,
                datasets[varname]["dims"],
                fill_value=datasets[varname]["atts"]["_FillValue"],
            )
        else:
            dat = ncfile.createVariable(varname, dtype, datasets[varname]["dims"])
        dat[:] = datasets[varname]["data"]
        # variable attributes
        if "atts" in datasets[varname]:
            for att in datasets[varname]["atts"]:
                if att != "_FillValue":
                    dat.__setattr__(
                        att, datasets[varname]["atts"][att]
                    )  # _FillValue is made in 'createVariable'
    # global attributes
    for key in atts:
        ncfile.__setattr__(key, atts[key])
    ncfile.close()
    logging.info("Wrote out " + output_file)

    if gzip:
        if wait:
            s = call(["gzip", "-f", output_file])  # ==wait to finish
        else:
            s = Popen(["gzip", "-f", output_file])  # ==will run in background

    logging.info("Process ended")
    return True


#####################################################################################################
def get_area_definition(
    projection_file, outny=-1, outnx=-1, return_latlons=False, return_xy=False
):
    from pyproj import Proj
    import pyresample as pr
    import numpy.ma as ma

    logging.info(f"Getting AreaDefinition from {projection_file}")

    nc = Dataset(projection_file)
    gip = nc.variables["goes_imager_projection"]
    x = nc.variables["x"][:]
    y = nc.variables["y"][:]

    # p = Proj('+proj=geos +lon_0='+str(gip.longitude_of_projection_origin)+\
    #         ' +h='+str(gip.perspective_point_height)+' +x_0=0.0 +y_0=0.0 +a=' + \
    #         str(gip.semi_major_axis) + ' +b=' + str(gip.semi_minor_axis) + ' +sweep=x')

    x *= gip.perspective_point_height
    y *= gip.perspective_point_height
    # print(x.min(),x.max())
    # xx,yy = np.meshgrid(x,y)
    ny, nx = len(y), len(x)  # np.shape(xx)
    # newlons, newlats = p(xx, yy, inverse=True)
    # mlats = ma.masked_where((newlats < -90) | (newlats > 90),newlats)
    # mlons = ma.masked_where((newlons < -180) | (newlons > 180),newlons)
    # print(mlons.max(),mlons.min())
    # newx,newy = p(mlons,mlats)
    # print(newx.min(),newx.max(),newy.min(),newy.max())
    # max_x = newx.max(); min_x = newx.min(); max_y = newy.max(); min_y = newy.min()
    # half_x = (max_x - min_x) / newlons.shape[1] / 2.
    # half_y = (max_y - min_y) / newlats.shape[0] / 2.
    # extents = (min_x - half_x, min_y - half_y, max_x + half_x, max_y + half_y)
    # print(min_x,max_x)
    extents = (x.min(), y.min(), x.max(), y.max())
    if outny > 0:
        # Increase or decrease spatial resolution. Note that outny and outnx should be
        # a whole-number multiple of ny and nx.
        # assert(ny % outny == 0 and nx % outnx == 0)
        ny = outny
        nx = outnx

    newgrid = pr.geometry.AreaDefinition(
        "geos",
        "goes_conus",
        "goes",
        {
            "proj": "geos",
            "h": gip.perspective_point_height,
            "lon_0": gip.longitude_of_projection_origin,
            "a": gip.semi_major_axis,
            "b": gip.semi_minor_axis,
            "sweep": gip.sweep_angle_axis,
        },
        nx,
        ny,
        extents,
    )
    nc.close()

    if return_latlons:
        return newgrid, ny, nx, newlons, newlats
    if return_xy:
        return newgrid, ny, nx, x, y
    else:
        return newgrid, ny, nx


########################################################################################################
def bytescale(data_arr, vmin, vmax):
    assert vmin < vmax
    DataImage = np.round((data_arr - vmin) / (vmax - vmin) * 255.9999)
    DataImage[DataImage < 0] = 0
    DataImage[DataImage > 255] = 255
    return DataImage.astype(np.uint8)

########################################################################################################
def unbytescale(scaled_arr, vmin, vmax):
    assert vmin < vmax
    scaled_arr = scaled_arr.astype(np.float32)
    unscaled_arr = scaled_arr / 255.9999 * (vmax - vmin) + vmin
    return unscaled_arr

########################################################################################################
def plax(
    lats,
    lons,
    satlon=-75.2,
    elevation=9000.0,
    gip=None,
    return_dict=False,
    write_plax_file=False,
):
    # By default, it will only return the parallax-corrected lats and lons.

    # elevation is height of object, in meters, above earth surface (assuming constant height)
    # ----->Local constants
    if np.ma.is_masked(lats) or np.ma.is_masked(lons):
        mask = lats.mask  # to be used later
        masked = True
    else:
        masked = False

    logging.info(
        f"Performing parallax correction with satlon = {satlon} deg. and elevation = {elevation} m."
    )
    to_radians = np.pi / 180.0  # Conversion to radians from degrees
    to_degrees = 180.0 / np.pi  # Conversion to degrees from radians
    right_angle = np.pi / 2.0  # Right angle in radians for reference
    satlat = 0.0  # Satellite latitude; 0.0 for GEOs
    satlat_rad = satlat * to_radians  # Satellite latitude in radians
    if gip:
        earth_radius = (gip["semi_major_axis"] + gip["semi_minor_axis"]) / 2.0
        altitude = earth_radius + gip["perspective_point_height"]
    else:
        earth_radius = 6371009.0  # Mean earth radius, in meters, based on WGS-84 data
        altitude = 42166111.9  # Distance of satellite, in meters, from center of earth

    earth_radius_elevation = (
        earth_radius + elevation
    )  # Mean radius of the earth plus height of object above surface, in meters
    satlon_rad = satlon * to_radians

    # ----->General variables defined
    datalat_rad = lats * to_radians
    datalon_rad = lons * to_radians

    datalat_pc_rad = np.zeros(lats.shape) - 999.0
    datalon_pc_rad = np.zeros(lons.shape) - 999.0

    # ----->Calculate the distance between satellite nadir and base of object (using haversine formula)
    londiff = satlon_rad - datalon_rad
    latdiff = satlat_rad - datalat_rad

    centralangle = 2.0 * np.arcsin(
        np.sqrt(
            (np.sin(latdiff / 2.0)) ** 2
            + np.cos(satlat_rad) * np.cos(datalat_rad) * (np.sin(londiff / 2.0)) ** 2
        )
    )
    gcdistance = earth_radius * centralangle

    # ----->Calculate the central angle that subtends the great circle distance between nadir and true position
    # ...First find distance between satellite and non-true position using the Law of Cosines
    satviewdist = np.sqrt(
        altitude**2
        + earth_radius**2
        - 2.0 * altitude * earth_radius * np.cos(centralangle)
    )

    # ...Then find the satellite view angle from nadir on great circle plane also using the Law of Cosines
    satviewangle = np.arccos(
        (earth_radius**2 - altitude**2 - satviewdist**2)
        / (-2.0 * altitude * satviewdist)
    )

    # ...Then find the adjusted central angle for parallax
    # First find angle between satellite and center of the earth where the true position is the vertex using the Law of Sines
    angleSNO = np.arcsin((altitude * np.sin(satviewangle)) / earth_radius_elevation)
    ind = np.where(angleSNO < right_angle)
    if len(ind) > 0:
        angleSNO[ind] = np.pi - angleSNO[ind]

    # Then calculate adjusted central angle for parallax using identity that all angles of a triangle add up to pi radians
    sat_true_centralangle = np.pi - angleSNO - satviewangle
    sat_true_gcdist = earth_radius * sat_true_centralangle

    # ----->Calculate latitudinal component of parallax correction (assumes great circle is equivalent to satellite meridian)
    # ...First find distance between satellite and non-true latitude position using the Law of Cosines
    satviewdist_lat = np.sqrt(
        altitude**2
        + earth_radius**2
        - 2.0 * altitude * earth_radius * np.cos(datalat_rad)
    )

    # ...Then find the satellite view zenith angle from nadir also using the Law of Cosines
    satviewangle_lat = np.arccos(
        (earth_radius**2 - altitude**2 - satviewdist_lat**2)
        / (-2.0 * altitude * satviewdist_lat)
    )

    # ...Then find the adjusted zenith angle for parallax
    # First find angle between satellite and center of the earth where the true position is the vertex using the Law of Sines
    angleSNO_lat = np.arcsin(
        (altitude * np.sin(satviewangle_lat)) / earth_radius_elevation
    )
    ind = np.where(angleSNO_lat < right_angle)
    if len(ind[0]) > 0:
        angleSNO_lat[ind] = np.pi - angleSNO_lat[ind]

    # Then calculate adjusted zenith angle for parallax using identity that all angles of a triangle add up to pi radians
    ind = np.where(lats > satlat)
    other_ind = np.where(lats <= satlat)
    if len(ind[0]) > 0:
        datalat_pc_rad[ind] = np.pi - angleSNO_lat[ind] - satviewangle_lat[ind]

    if len(other_ind) > 0:
        datalat_pc_rad[other_ind] = (
            angleSNO_lat[other_ind] + satviewangle_lat[other_ind] - np.pi
        )

    # ----->Calculate longitudinal component of parallax correction (using haversine formula)
    latdiff_pc = satlat_rad - datalat_pc_rad
    ind = np.where(lons < satlon)
    other_ind = np.where(lons >= satlon)
    if len(ind[0]) > 0:
        datalon_pc_rad[ind] = satlon_rad - 2.0 * np.arcsin(
            np.sqrt(
                np.abs(
                    (
                        (np.sin(sat_true_centralangle[ind] / 2.0)) ** 2
                        - (np.sin(latdiff_pc[ind] / 2.0)) ** 2
                    )
                    / (np.cos(satlat_rad) * np.cos(datalat_pc_rad[ind]))
                )
            )
        )
    if len(other_ind[0]) > 0:
        datalon_pc_rad[other_ind] = satlon_rad + 2.0 * np.arcsin(
            np.sqrt(
                np.abs(
                    (
                        (np.sin(sat_true_centralangle[other_ind] / 2.0)) ** 2
                        - (np.sin(latdiff_pc[other_ind] / 2.0)) ** 2
                    )
                    / (np.cos(satlat_rad) * np.cos(datalat_pc_rad[other_ind]))
                )
            )
        )

    # ----->Place parallax-corrected latitudes and longitudes into respective arrays
    lat_pc = datalat_pc_rad * to_degrees
    lon_pc = datalon_pc_rad * to_degrees

    if masked:
        lat_pc = np.ma.MaskedArray(lat_pc, mask=mask)
        lon_pc = np.ma.MaskedArray(lon_pc, mask=mask)


    if not (return_dict) and not (write_plax_file):
        logging.info("Process ended.")
        return lat_pc, lon_pc

    else:
        # NB: NW corner should be the 0,0 point for your lats and lons
        logging.info("Getting new xinds (for lons) and yinds (for lats)")

        latdiff = lats - lat_pc
        londiff = lons - lon_pc
        nlats, nlons = lons.shape
        xind = np.zeros((nlats, nlons), dtype=int)
        yind = np.zeros((nlats, nlons), dtype=int)

        t1 = time.time()
        mask = (
            np.ma.is_masked(lats[1:-1, 1:-1])
            | np.ma.is_masked(lats[:-2, 1:-1])
            | np.ma.is_masked(lats[2:, 1:-1])
            | np.ma.is_masked(lons[1:-1, 1:-1])
            | np.ma.is_masked(lons[1:-1, :-2])
            | np.ma.is_masked(lons[1:-1, 2:])
        )

        dy = (lats[:-2, 1:-1] - lats[2:, 1:-1]) / 2.0
        dx = (lons[1:-1, :-2] - lons[1:-1, 2:]) / 2.0

        latshift = np.round(latdiff[1:-1, 1:-1] / dy)  # number of pixels to shift
        lonshift = np.round(londiff[1:-1, 1:-1] / dx)  # number of pixels to shift

        new_elem = np.arange(1, nlons - 1) + lonshift  # add vector to each column
        new_line = (
            np.arange(1, nlats - 1).reshape(-1, 1) + latshift
        )  # reshape so that we add to each row

        xind[1:-1, 1:-1] = new_elem
        yind[1:-1, 1:-1] = new_line

        logging.info("Accounting for pixels off the grid")

        # Account for edges
        yind[0, :] = yind[1, :]
        yind[-1, :] = yind[-2, :]
        yind[:, 0] = yind[:, 1]
        yind[:, -1] = yind[:, -2]
        xind[0, :] = xind[1, :]
        xind[-1, :] = xind[-2, :]
        xind[:, 0] = xind[:, 1]
        xind[:, -1] = xind[:, -2]

        # Account for pixels off the grid
        yind[yind >= nlats] = nlats - 1
        yind[yind < 0] = 0
        xind[xind >= nlons] = nlons - 1
        xind[xind < 0] = 0

        outdata = {
            "xind": xind,
            "yind": yind,
            "lat_orig": lats,
            "lon_orig": lons,
            "lat_pc": lat_pc,
            "lon_pc": lon_pc,
            "elevation_in_m": elevation,
            "satlon": round(satlon, 1),
            "dx": f"{np.round(lons[0,1] - lons[0,0],2) * 100}km",
            "dy": f"{np.round(lats[0,0] - lats[1,0],2) * 100}km",
        }

        # import matplotlib.pyplot as plt
        # fig,ax=plt.subplots(nrows=1,ncols=2,figsize=(16,9))
        # im = ax[0].imshow(latshift); ax[0].set_title('latshift'); plt.colorbar(im,ax=ax[0],shrink=0.5)
        # im = ax[1].imshow(lonshift); ax[1].set_title('lonshift'); plt.colorbar(im,ax=ax[1],shrink=0.5)
        # plt.savefig('tmp.png',bbox_inches='tight')
        # sys.exit()

        if return_dict:
            return outdata

        if write_plax_file:
            outfile = "PLAX_" + "{:.1f}".format(satlon) + f"_{int(elevation)}m.pkl"
            pickle.dump(outdata, open(outfile, "wb"))
            logging.info(f"Wrote out {outfile}")

####################################################################################################
def calculate_abi_degrees(file_id):

    """
    Calculate latitude and longitude from GOES ABI fixed grid projection data
    GOES ABI fixed grid projection is a map projection relative to the GOES satellit
    Units: latitude in °N (°S < 0), longitude in °E (°W < 0)
    See GOES-R Product User Guide (PUG) Volume 5 (L2 products) Section 4.2.8 for details & example of calculation
    "file_id" is an ABI L1b or L2 .nc file opened using the netCDF4 library
    This function was created by NOAA/NESDIS/STAR Aerosols and Atmospheric Composition Science Team.
    """
    
    # Read in GOES ABI fixed grid projection variables and constants
    x_coordinate_1d = file_id.variables['x'][:]  # E/W scanning angle in radians
    y_coordinate_1d = file_id.variables['y'][:]  # N/S elevation angle in radians
    projection_info = file_id.variables['goes_imager_projection']
    lon_origin = projection_info.longitude_of_projection_origin
    H = projection_info.perspective_point_height+projection_info.semi_major_axis
    r_eq = projection_info.semi_major_axis
    r_pol = projection_info.semi_minor_axis
    
    # Create 2D coordinate matrices from 1D coordinate vectors
    x_coordinate_2d, y_coordinate_2d = np.meshgrid(x_coordinate_1d, y_coordinate_1d)
    
    # Equations to calculate latitude and longitude
    lambda_0 = (lon_origin*np.pi)/180.0  
    a_var = np.power(np.sin(x_coordinate_2d),2.0) + (np.power(np.cos(x_coordinate_2d),2.0)*(np.power(np.cos(y_coordinate_2d),2.0)+(((r_eq*r_eq)/(r_pol*r_pol))*np.power(np.sin(y_coordinate_2d),2.0))))
    b_var = -2.0*H*np.cos(x_coordinate_2d)*np.cos(y_coordinate_2d)
    c_var = (H**2.0)-(r_eq**2.0)
    r_s = (-1.0*b_var - np.sqrt((b_var**2)-(4.0*a_var*c_var)))/(2.0*a_var)
    s_x = r_s*np.cos(x_coordinate_2d)*np.cos(y_coordinate_2d)
    s_y = - r_s*np.sin(x_coordinate_2d)
    s_z = r_s*np.cos(x_coordinate_2d)*np.sin(y_coordinate_2d)
    
    # Ignore numpy errors for sqrt of negative number; occurs for GOES-16 ABI CONUS sector data
    np.seterr(all='ignore')
    
    abi_lat = (180.0/np.pi)*(np.arctan(((r_eq*r_eq)/(r_pol*r_pol))*((s_z/np.sqrt(((H-s_x)*(H-s_x))+(s_y*s_y))))))
    abi_lon = (lambda_0 - np.arctan(s_y/(H-s_x)))*(180.0/np.pi)
    
    return abi_lat, abi_lon
