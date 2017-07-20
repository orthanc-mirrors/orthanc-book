docker build -t orthanc-book-builder .
docker run --rm -v $(pwd):/app orthanc-book-builder

docker rmi orthanc-book-builder  # since we rebuild it anyway, no need to keep it -> don't accumulate <none> images