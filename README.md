![example workflow](https://github.com/fibboo/foodgram-project-react/actions/workflows/workflow.yaml/badge.svg)

# Foodgram
## About:
Food Assistant app. The site where users will post recipes, add
other people's recipes to favorites and subscribe to publications of other authors. The shopping list service will allow
users to create a list of products that need to be bought for the preparation of selected dishes.
<br><br>
There was a ready frontend on React and API documentation (in folder docs). The task was to make a backend on Django REST Framework and run it in Docker with frontend.
<br><br>
You can visit demo here https://foodgram.fibboo.space/ <br>

## Requirements:
docker https://docs.docker.com/engine/install/ <br>
docker-compose https://docs.docker.com/compose/install/

## How to run:

Clone project and cd to infra
```
git clone git@github.com:fibboo/foodgram-project-react.git
```
Create .env file as in the template infra/.env.template <br>
Change domains in infra/default.conf to yours <br>
Don't forget to set up DNS with your domain registrar<br>

Push for magic to happen

After first deploy migrate and collect static.
```
sudo docker-compose exec backend python manage.py migrate
sudo docker-compose exec backend python manage.py collectstatic
```

Login to your server, and run init-letsencrypt.sh. This script will get ssl for your domain
```
ssh user@your-server-ip
cd infra/
chmod +x init-letsencrypt.sh
sudo ./init-letsencrypt.sh
```

## Thanks
Thank Phillip for his instruction on how to get ssl with nginx, Let’s Encrypt, certbot and Docker https://pentacent.medium.com/nginx-and-lets-encrypt-with-docker-in-less-than-5-minutes-b4b8a60d3a71 <br>
