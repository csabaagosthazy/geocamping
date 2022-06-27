# Geocamping
Web application for a camping site using GIS python, Leaflet and 
This application was created as a university project by
Babaiantz Mathias, Agosthazy Csaba, Pinto de Matos Daniel

It represents a camping site with different geospatial layers.
The main takeaway is discovering gis python libraries and using different geometries and geospatial functions.

# Geospatial layers

To represent the camping site 6 different layers are created using Qgis. 
![image](https://user-images.githubusercontent.com/40959918/175899102-55378cb5-a85c-4dd3-ad08-4fdeccddaf11.png)

Zones: camping zones, ie. beach zone, parking, lease zones... etc
Facilities: camping facilities, utilities, bars, the restaurant ...etc
Services: Services outside of the camping, port, bus station, shops ...etc
Cottages: rentable cottages
Bungalows: rentable bungalows
Slots: rentable tent slots

([Shape files](camping_shp.zip))

#Database

![image](https://user-images.githubusercontent.com/40959918/175900675-1f376284-5664-4583-a5d1-39af32bdc20a.png)
![image](https://user-images.githubusercontent.com/40959918/175900792-7be44d8c-d440-4aa5-8839-38f27e5b581b.png)

All the layers are saved in the database, PostgreSQL with PostGIS extension. 
This allows to store geometry (geom) files in the database.

([SQL scripts](SQL_scripts.zip))

#API

With GIS Python a basic API is created to communicate with the database.
This handles all request and responses plus make geospatial calculations.

With GIS python there are many functions for geometry, such as area, distance calculation... etc. 
Here there are only a few implemented.

([Postman api doc](geocamping.postman_collection.json))

#User interface

The user interface leaflet was used to create the map and show different layers.
![image](https://user-images.githubusercontent.com/40959918/175903423-4bd1169c-659d-442b-aef9-705c2c2d1ef7.png)

Also, some details can be found about the camping, and more information is revealed by hovering over the rentable items.





