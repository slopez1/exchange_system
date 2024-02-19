FROM ethereum/client-go:v1.11.6

# Update apk repositories and install nodejs
RUN apk update 

# Install nodejs (npm is included), git, bash, and perl
RUN apk add --no-cache nodejs git bash perl npm


RUN cd /root &&\
    git clone https://github.com/cubedro/eth-net-intelligence-api &&\
    cd eth-net-intelligence-api &&\
    npm install &&\
    npm install -g pm2

ADD start.sh /root/start.sh
ADD app.json /root/eth-net-intelligence-api/app.json
RUN chmod +x /root/start.sh

ENTRYPOINT /root/start.sh
