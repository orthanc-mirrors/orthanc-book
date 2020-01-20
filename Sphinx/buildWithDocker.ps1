# This has been tested with Docker for Windows CE version 2.0.0.2 (30215)
# on Windows 10 Pro x64 (10.0.17134) with stock Powershell (5.1)

docker build -t orthanc-book-builder .

$pwdSlash = $pwd.Path.Replace("\","/")
docker run --rm -v "$($pwdSlash):/app" orthanc-book-builder

docker rmi orthanc-book-builder  # since we rebuild it anyway, no need to keep it -> don't accumulate <none> images
