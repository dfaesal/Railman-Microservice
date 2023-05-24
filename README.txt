#Run Servers:(change ip)
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
uvicorn main:app --host 0.0.0.0 --port 8002 --reload

#Build Images:
docker build -t order .
docker build -t user .
docker build -t payment .

#Create Network
docker network create my-network

#Run Containers:
docker run -d -p 8000:8000 --name user-app --network my-network --network-alias user-app user 
docker run -d -p 8001:8001 --name order-app --network my-network --network-alias order-app order 
docker run -d -p 8002:8002 --name payment-app --network my-network --network-alias payment-app payment 
docker run -d -p 27017:27017 --name mongodb_container -v "D:\Fullstack Course\Slides\Cloud Native Apps\Assignment\Assignment - 2\data\:/data/db" --network my-network --network-alias mongodb mongo
