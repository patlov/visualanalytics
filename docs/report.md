# VISUAL ANALYTICS SS21 - Project Report

#### Group 20

David Kerschbaumer 11708776<br/>
Patrick Lovric 11707313<br/>
Maximilian Theiner 11714265<br/>



## Motivation and Goals

In this project we want to visualize the data of [sensor.community](https://sensor.community/en/) in an clear and easy to understand way. Our tool provides basic functionality, like looking for a specific sensor in a specific time range and watch the measurements visually, as well as advanced visualization techniques, like clustering of similar sensors or anomaly search. 



## Design of our Solution

### Backend

### Frontend 

## Description of our Implementation

#### Downloading

#### Geo Clustering

For every sensor we have a position as latitude and longitude. We used the HERE maps reverse geocoder (https://developer.here.com/documentation/geocoder/dev_guide/topics/what-is.html) to tranform this position into a classifiable country information. For every position we got the countryname (e.g. AUT for Austria), statename (e.g. Styria) and cityname (e.g. Graz). This enabled us to cluster every sensor into the corresponding geographic category. By packing every sensor in a large dictonary, we could retrieve sensors for specific regions of the world and implement sophisticated query algorithms for example: “query two sensors for every city in the world”. See clutering.py and here.py for more information.

#### Finding similarities and anomalies

With our frontend and the capability to select sensors by geographic region we made it easy for the user to select sensors of interest with a high degree of precision. The next task was to find similarities and anomalies for a bunch of selected sensors. We did this with K-Means, one of the most known algorithms for clustering data. K-Means creates centroids and assigns them suitable candidates by minimizing the distance. However, we had a problem with the distance calculation between single timeseries measurements. They had different lengths and sampling rates. To solve this issue, we used Dynamic Time Warping (DTW) to calculate the distance between timeseries that are non-linearly warped along the time dimension. We combined K-Means and DTW to cluster a bunch of timeseries into n clusters. The user must choose the number of clusters that he wants. The K-Means algorithm now clusters the timeseries dataset into n clusters until convergence is reached. After executing we have n cluster centroids and every timeseries in the dataset is assigned to one of these centroids.

#### DB-Index

The next step is to identify clusters that can be classified as anomalies and clusters that give a hint to similarities. To do that we needed metric that indicates how unique a cluster is. There are several ways to implement such a cluster analysis, we chose the so called DB-index (https://en.wikipedia.org/wiki/Davies%E2%80%93Bouldin_index). Clusters with a low DB-index can be seen as unique and good cluster approximation.

## Use case description



## Discussion and Outlook





