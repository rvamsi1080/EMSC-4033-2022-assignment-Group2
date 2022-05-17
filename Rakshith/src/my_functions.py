"""
Functions we would like to test should be consistent with Rakshith/src/my_functions

"""

from .dependencies import *




def my_documentation():

    markdown_documentation = """ 
    This function returns a Markdown document explaining information of this program. 
    
# Map plotting

In this notbook, we attempt at plotting a high-resolution map at the region of 30-40°N, 113-123°W. The map is supposed to display a variety of information containing coastlines and water features, locations of past earthquake events within the set time range, seafloor age and topography on the basemap. The following explains more information about how each element of the map is obtained and plotted.
    
##  Basemap

Firstly, image tiles are required to produce the basemap. `cartopy` implements the functionality to get access to various sources providing map image tiles. 
[Mapbox](https://docs.mapbox.com/api/maps/styles/) provides a lot of map styles to choose from. In our program, we use **Mapbox outdoors**, which gives out vivid natural features, topopraphy as well as roadways and built fatures. We need to login into mapbox [website](https://docs.mapbox.com/api/maps/styles/) to get the required `access_token`.

The full list of image tiles and their sources can be found in the source code in [Github](https://github.com/SciTools/cartopy/blob/master/lib/cartopy/io/img_tiles.py).

## Coastlines and water features

Subsequently, coastlines and other water features like lakes, rivers and the ocean are added to the basemap. `cartopy.feature.NaturalEarthFeature` provides the necessary interfaces to obtain them at a specified resolution, i.e. ‘10m’, ‘50m’, or ‘110m’ corresponding to a scale of 1:10,000,000, 1:50,000,000, and 1:110,000,000 respectively. In this program, the coastlines are plotted at the resolution of '10m' and the water features are plotted at the resolution of '50m'.

## Earthquake events 

10-year records (2002-2012) of earthquakes that occurred within a specified region are collected and used in the program. The records of earthquake events are fed into the program as point data from **IRIS** (Incorporated Research Institution for Seismology) by caliing the functions from `obspy` package. Each point datum consists of 4 parameters: longitude, latitude, depth of the origin and magnitude of the earthquake.

## Seafloor Age

Data pertaining to the age of the sea floor are stored on `Cloudstor`, which provides cloud storage service helping people anywhere in the world tp upload and download data. Seafloor age information is displayed on the map applying a diverging colormap from red to blue.

"""
    
    return markdown_documentation



def my_coastlines(resolution):
    """ This function returns the necessary coastlines at the requested resolution """
    import cartopy.feature as cfeature
    coastline = cfeature.NaturalEarthFeature('physical', 'coastline', resolution,
                           edgecolor=(0.0,0.0,0.0),
                           facecolor="none")
  


    return coastline


def my_water_features(resolution, lakes=True, rivers=True, ocean=False):
    """
    Returns a [list] of cartopy features at the requested resolution (10m, 50m or 110m)
    Furthermore, it can also be specified which water features to be returned
    
    """
    
    features = [] #returns an empty list for features
    
    import cartopy.feature as cfeature
    
    rivers_visible = cfeature.NaturalEarthFeature('physical', 'rivers', resolution,
                                        edgecolor='Blue', facecolor="none")
    lakes_visible = cfeature.NaturalEarthFeature('physical', 'lakes', resolution,
                                        edgecolor="blue", facecolor="blue")
    ocean_visible = cfeature.NaturalEarthFeature('physical', 'ocean', resolution,
                                        edgecolor="green",facecolor="blue")

    #the following code is to determine which water features are needed
    if rivers == True:
        features.append(rivers_visible)
        
    if lakes == True:
        features.append(lakes_visible)

    if ocean == True:
        features.append(ocean_visible)
    
    return features

def my_basemaps():
    """
    This function returns a dictionary of map tile generators that cartopy can use.
    It contains: "mapbox_outdoors", "open_street_map", which are necessary map titles
    for our program
    
    """
    
    ## The full list of available interfaces is found in the source code for this one:
    ## https://github.com/SciTools/cartopy/blob/master/lib/cartopy/io/img_tiles.py

    # dictionary of possible basemap tile objects
    
    mapper = {"open_street_map":3, "mapbox_outdoors":1}
    
    ## Open Street map
    mapper["open_street_map"] = cimgt.OSM()
    
    ##Open Outdoors map
    mapper["mapbox_outdoors"] = cimgt.MapboxTiles(map_id='outdoors-v11', access_token='pk.eyJ1IjoibG91aXNtb3Jlc2kiLCJhIjoiY2pzeG1mZzFqMG5sZDQ0czF5YzY1NmZ4cSJ9.lpsUzmLasydBlS0IOqe5JA')

    return mapper


## specify some point data (e.g. global seismicity in this case)

def download_point_data(region):
    """
    This function returns an np.array of earthquake features that consists of the longitude, latitude and depth of origins and earthquake magnitudes.
    The range of the earthquake occurring region should be input as the form of [min_lon, max_lon, min_lat, max_lat].
    
    """
    
    from obspy.core import event
    from obspy.clients.fdsn import Client
    from obspy import UTCDateTime
    
    #set data source

    client = Client("IRIS")

    

    from_time = UTCDateTime("2003-01-01")
    to_time   = UTCDateTime("2012-01-01")
    
    cat = client.get_events(starttime = from_time, endtime = to_time,
                           minlatitude = region[2],maxlatitude = region[3],
                            minlongitude = region[0],maxlongitude = region[1])

    print ("Point data: {} events in catalogue".format(cat.count()))
    
    # Unpack the obspy data into a plottable array

    event_count = cat.count()

    eq_origins = np.zeros((event_count, 4))

    for i in range(event_count):
        eq_origins[i][0] = cat[i].origins[0].longitude
        eq_origins[i][1] = cat[i].origins[0].latitude
        eq_origins[i][2] = cat[i].origins[0].depth
        eq_origins[i][3] = cat[i].magnitudes[0].mag

    return eq_origins


def my_point_data(region):
    """
    This is to download the required earthquake event data using the previously defined function: download_point_data().
    
    """
    
    data = download_point_data(region)
    
    return data


## - Some global raster data (lon, lat, data) global plate age, in this example

def download_raster_data():
    """
    Returns a np.array of seafloor ages with longitude and latitude.
    
    """
    # Seafloor age data and global image - data from Earthbyters

    # The data come as ascii lon / lat / age tuples with NaN for no data. 
    # This can be loaded with ...

    # age = numpy.loadtxt("Resources/global_age_data.3.6.xyz")
    # age_data = age.reshape(1801,3601,3)  # I looked at the data and figured out what numbers to use
    # age_img  = age_data[:,:,2]

    # But this is super slow, so I have just stored the Age data on the grid (1801 x 3601) which we can reconstruct easily

    from cloudstor import cloudstor
     # Download data from cloudstor
    teaching_data = cloudstor(url="L93TxcmtLQzcfbk", password='')
    teaching_data.download_file_if_distinct("global_age_data.3.6.z.npz", "global_age_data.3.6.z.npz")
    
    Ages = np.load("global_age_data.3.6.z.npz")["ageData"]

    datasize = (1801, 3601, 3)
    raster_data = np.empty(datasize)
    lats = np.linspace(90, -90, datasize[0])
    lons = np.linspace(-180.0,180.0, datasize[1])
    
    arrlons,arrlats = np.meshgrid(lons, lats)
    
    raster_data[...,0] = arrlons[...] # Longitude
    raster_data[...,1] = arrlats[...] # Latitude
    raster_data[...,2] = ages[...] # Add age data to the array

    return raster_data


def my_global_raster_data():
    """
    This downloads seafloor age data using the above defined function: download_raster_data().
     
     """

    raster = download_raster_data()
    
    return raster
