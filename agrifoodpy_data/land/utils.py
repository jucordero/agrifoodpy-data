import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import Point, MultiPoint
import xarray as xr

def raster_gdf(
    gdf: gpd.GeoDataFrame,
    value_column: str,
    name: str,
    resolution: float,
    crs: str = None,
    bounds: tuple = None,
    anchor: tuple = None
) -> xr.Dataset:
    """Rasterise a GeoDataFrame and return a xarray Dataset.

    Parameters
    ----------
    gdf : gpd.GeoDataFrame
        Input GeoDataFrame with geometries and values to rasterise.
    value_column : str
        Name of the column in gdf containing the values to rasterise.
    name : str
        Name for the output xarray DataArray.
    resolution : float
        Resolution of the output raster in meters.
    crs : str, optional
        Coordinate reference system to use for rasterisation. If None, the gdf's
        current CRS will be used.    
    bounds : tuple, optional
        Bounding box (minx, miny, maxx, maxy) to define the extent of the
        raster. If None, the bounds of the gdf will be used.
    anchor : tuple, optional
        (x_anchor, y_anchor) to anchor the bin boundaries. If None, defaults to
        (xmin, ymin) from bounds. Use (0, 0) to start bins at the origin.

    Returns
    -------
    xr.Dataset
        Rasterised data as an xarray Dataset.
    """
    
    # Ensure the GeoDataFrame is in the right CRS
    if crs is not None:
        gdf = gdf.to_crs(crs)

    target_crs = gdf.crs

    # Define the bounds for the rasterisation
    if bounds:
        xmin, ymin, xmax, ymax = bounds
    else:
        xmin, ymin, xmax, ymax = gdf.total_bounds

    gdf = gdf.cx[xmin:xmax, ymin:ymax]

    if anchor is None:
        anchor = (xmin, ymin)
    
    x_anchor, y_anchor = anchor

    size = np.ceil([(xmax - xmin)/resolution, (ymax - ymin)/resolution]).astype(int)

    binsx = np.arange(size[0] + 1) * resolution + x_anchor 
    binsy = np.arange(size[1] + 1) * resolution + y_anchor

    # Pixel center coordinates
    xcoords = 0.5 * (binsx[1:] + binsx[:-1])
    ycoords = 0.5 * (binsy[1:] + binsy[:-1])

    # Create and empty dataframe and fill the grid positions and indexes
    xxpos = np.tile(xcoords, len(ycoords))
    ix = np.tile(np.arange(size[0]), size[1])
    yypos = np.repeat(ycoords, len(xcoords))
    iy = np.repeat(np.arange(size[1]), size[0])

    df = pd.DataFrame({'xpos':ix, 'ypos':iy})
    df['geometry'] = list(zip(xxpos,yypos))
    df['geometry'] = df['geometry'].apply(Point)

    points = gpd.GeoDataFrame(df, crs=target_crs)
    
    # Create a dictionary with geometry names as keys and index as items
    gdf_unique_vals = np.unique(gdf[value_column])
    vals_index_dict = {name: idx for idx, name in enumerate(gdf_unique_vals)}

    # Find the points that fall within the boundary polygons
    within_bdry = gpd.sjoin(points, gdf, how='inner', predicate='within')
    
    # Assign the corresponding index
    within_bdry["_index"] = within_bdry[value_column].map(vals_index_dict)

    # Create an empty raster and fill in the corresponding index
    raster = np.ones((size[1], size[0]), dtype=np.uint8)*np.nan
    raster[tuple([within_bdry['ypos'], within_bdry['xpos']])] \
          = within_bdry['_index']

    # Create a dataset with x, y, and Region dimensions
    ds = xr.Dataset(
        data_vars={
            name: (["y", "x"], raster)
        },
        coords={
            "x": xcoords,
            "y": ycoords,
            "ID": list(vals_index_dict.values()),
            "Region": ("ID", list(vals_index_dict.keys())),
        },
    )

    return ds