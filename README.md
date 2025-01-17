# Flight Crew Member simulation


Build docker image
```
docker build -t airline-crew-mgmt .
```

Run docker image
```
docker run -it -v $(pwd):/mounted --rm airline-crew-mgmt

cd /mounted
python main.py
```
