# VISUAL ANALYTICS SS21 - Project Report

#### Group 20

David Kerschbaumer 11708776<br/>
Patrick Lovric 11707313<br/>
Maximilian Theiner 11714265<br/>



## Motivation and Goals

In this project we created GeoCluster Visualizer, a tool to visualise the data of [sensor.community](https://sensor.community/en/) in an clear and easy understandable way. Our tool provides basic functionality, like looking for a specific sensor in a specific time range and watch the measurements visually, as well as advanced visualisation techniques, like clustering of similar sensors or find weather anomalies.

One of our main goals was to use the largest available data set and be able to present the user all available data from [sensor.community](https://sensor.community/en/) . We started by downloading the data set from their archive http://archive.sensor.community/ but quickly realised, that the data set is many hundred Gigabyte large. We had to came up with an idea to crawl the data in real time as fast as possible, which we describe at [Downloading](#Downloading) in more detail. 

Even crawling the data in real time takes more time, we found it more challenging and interesting for user experience  to have current measurements in contrast to a fixed data set from the past. 

We focus on time series visualisation, but we tried to present the data also in other ways, like we do at the [worldmap](#Worldmap). 

## Program Design

### Infrastructure

We implemented the application GeoClima in python with the IDE PyCharm from JetBrains.  For visualisation and the frontend we used the python library [Plotly](https://plotly.com/), which delivers easy to use methods with much functionality.  

Some functionality, like API requests or sensor downloads, are implemented multiprocessed using the python library aiohttp and asyncio. 

### Frontend 

The frontend of our application GeoClima consists of 4 Tabs with different functionalities: [Worldmap](#Worldmap), [Similarities](#Similarities), [Timeseries](#Timeseries) and [Anomaly](#Anomaly). 

#### Worldmap

In this tab we get, for every federal state in the world, which sends sensor data, one sensor and display
it over the whole map. We reduced it to specific sensor types (`'bme280', 'dht22', 'bmp280'`) which only send temperature and humidity data. The reason
being for that, is we wanted to reduce the amount of requests we would send to the server and also usability.

The sensor data displayed shows the average of the last 5 minutes and can be refreshed by the button on the top-right with
the name `refresh`. On the top-left you can choose which type of sensor you want to display on the map. 
Now if you click onto a sensor, it will move you to the tab time-series where you choose a time window (from / to-time)
and the sensor gets plotted as 3D-graph with `temperature` and `humidity` corresponding the a specific time.


#### Similarities

In this tab we show the user similar measurements by clustering the sensor data and present it. Some input fields are required (marked with *) and some are optional. 

After the user enters the required time range (from-to) and the type of measurement (`temperature` or `humidity`) we randomly select one sensor of each country in our database and cluster these results with k-means. More about the clustering process is described in [Finding similarities and anomalies](#Finding similarities and anomalies). As result the user gets presented k clusters (the default value for k is 4) sorted by their similarity, calculated with [DB-Index](#DB-Index). 

This features allows us to explore different kind of similarities between cities which are far from each other and e.g. we can see that the temperature in Toronto behaves same es in Graz. 

For more specific requests GeoClima supports optional input fields like `Country` , `State` , `Number of sensors per Region` and `Number of Clusters` .  If `Country` and/or `State` is provided we only search for similarities in this region. One can increase the granularity of sensors by increasing the `Number of sensors per Region`. 

On the right GeoClima provide some additional information about the current user request, like the number of observed sensors, the selected input fields and the DB Index of the clusters. With this information one can easily see how different the clusters are. 

#### Timeseries

In this tab we can look at many sensors which are in the same City, and look for similar patterns in the timeseries and maybe detect outliers or
sensors which are defect or not behaving in the intended way.

Either you get to the timeseries tab via clicking onto a sensor on the worldmap - then choose the `from-time` and the
`to-time`

or

You start by clicking in which `country`, federal `state`, `city`, `sensor type`, `sensor ID` and `measurement value` you want to display. 

By selecting all the given dropdowns or clicking the sensor on the map, we get the sensor_id(s) and based on the
from-time, to-time and the sensor_id(s), we check if the same sensordata is in the cache. If yes we use it, otherwise 
GeoClima downloads all the data in the background and then plots the graph(s) on the website.

You cannot generate a linechart without specifying all the dropdown fields, except you choose a sensor from the map.

Additonally we added the functionality to display the sensor data in 3D. In this case `Type of Measurement` is not considered, because `temperature` and `humidity` are represented in the 3D graph, corresponding the the given time range. 


#### Anomaly

In the anomaly-tab we display anomaly behaviour of sensors. This can be because of anomaly weather conditions, as well as from incorrect measurement. Again the user enters the time range and the type of measurement (`temperature` or `humidity`) and we randomly select one sensor of each country in our database to find anomalies between countries.

After clicking submit, very similar to our similarities search, we compute clusters with the k-means algorithm, whereat k equals 5. But here we calculate the dissimilarity between clusters and present the most unique cluster as an anomaly. The other computed clusters were merged together as a second cluster to have a better overview and comparison to the anomaly. 

We also support specific requests with optional input fields `Country` and `State` to find anomalies in a specific location. If `Country` and/or `State` is provided we increase the number of observed sensors to have meaningful results. 

As in the similarities view we again provide on the right some additional information about the current user request and the DB Index of the anomaly cluster. 

## Implementation

#### Downloading

Sensorcommunity is organised in a large folder structure that represents a tree with year, months and day. In the lowest layer of the tree structure the according sensor measurements for a day are saved. There are different types of sensors (e.g. bmp280) for different vectors (e.g. temperature, humidity ..). We query a sensor for a day by building the corresponding URL with buildCSVurl. </br>

The user can specify start_date, end_date in the frontend and we generate a every file url from this input. After creating the links for every sensor, we download them multiprocessed by creating a Pool for every CPU core. This allows faster download speeds.

#### Preprocessing

In preprocess.py we do a lot of preprocessing before we actually cluster the data. Preprocessing consists of following steps:

* Sort daily dataframe by time
* use timestamp as index
* cat dataframes together
* resample dataframe
* drop NaN values
* interpolate data to fill small gaps

#### Geo Clustering

For every sensor we have a position as latitude and longitude. We used the HERE maps reverse geocoder (https://developer.here.com/documentation/geocoder/dev_guide/topics/what-is.html) to transform this position into a classifiable country information. For every position we got the country name (e.g. AUT for Austria), state name (e.g. Styria) and city name (e.g. Graz). This enabled us to cluster every sensor into the corresponding geographic category. By packing every sensor in a large dictionary, we could retrieve sensors for specific regions of the world and implement sophisticated query algorithms for example: “query two sensors for every city in the world”. See [clutering.py](../clustering.py) and [here.py](../here.py) for more information.

#### Finding similarities and anomalies

With our frontend and the capability to select sensors by geographic region we made it easy for the user to select sensors of interest with a high degree of precision. The next task was to find similarities and anomalies for a bunch of selected sensors. We did this with K-Means, one of the most known algorithms for clustering data. K-Means creates centroids and assigns them suitable candidates by minimizing the distance. However, we had a problem with the distance calculation between single timeseries measurements. They had different lengths and sampling rates. To solve this issue, we used Dynamic Time Warping (DTW) to calculate the distance between timeseries that are non-linearly warped along the time dimension. We combined K-Means and DTW to cluster a bunch of timeseries into n clusters. The user must choose the number of clusters that he wants. The K-Means algorithm now clusters the timeseries dataset into n clusters until convergence is reached. After executing we have n cluster centroids and every timeseries in the dataset is assigned to one of these centroids.

#### DB-Index

The next step is to identify clusters that can be classified as anomalies and clusters that give a hint to similarities. To do that we needed metric that indicates how unique/good a cluster is. There are several ways to implement such a cluster analysis, we chose the so called DB-index (https://en.wikipedia.org/wiki/Davies%E2%80%93Bouldin_index). Clusters with a low DB-index can be seen as unique and good cluster approximation.



## Conclusion

In this project we created an application called GeoCluster. The most challenging part was to have a solid structure for crawling the data in real time and deliver it in an appropriate time to the frontend. It took us weeks to find the best solution for crawling data with csv-files. Of course, it would have been easier if we would have downloaded a part of the database once and then processed it, but we found it more interesting for users to display up-to-date data. We also implemented the world map, which delivers real-time sensor data from the last 5 minutes of all sensors around the world.

Problems occur, as already mentioned, mostly at crawling the huge amount of data. Sometimes the sensors were invalid or had an other form, some measurements were invalid (a temperature of -140 degree of a sensor in Italy) and sometime the API banned us temporary because of too many requests. Latter would be our net next for improvement for having a more solid version of our application.

If more time would have been available we also would have implemented other data visualisation techniques with glyphs and added functionality to find more anomalies.




