docker rm orthanc-book-builder-container
docker build -t orthanc-book-builder .
docker run --name=orthanc-book-builder-container orthanc-book-builder
docker cp orthanc-book-builder-container:/app/build .