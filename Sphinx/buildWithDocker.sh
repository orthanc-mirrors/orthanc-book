docker build -t orthanc-book-builder .
docker run --rm -v $(pwd):/app orthanc-book-builder