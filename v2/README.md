# CloserGeographicallyPointsAPI

To run the dockerized API, follow the steps bellow.

1. Build the API image.
    - ``sudo docker build --tag closer_geo_point_api .``
2. Check if the image was successfully builded.
    - ``sudo docker images | grep closer_geo_point_api``
3. Run the docker image.
    - ``sudo docker run -p 8040:8040 --name closer_points_api closer_geo_point_api``
