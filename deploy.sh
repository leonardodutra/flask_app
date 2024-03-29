docker build --pull --rm -f "Dockerfile" -t pixnonimo:latest "."
docker run --publish 5000:5000 pixnonimo:latest