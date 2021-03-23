# Variables
CONFIG_NAME=personalSite

buildPushUp: buildAWS pushAWS awsUp
buildPush: build push

createConfig:
	ecs-cli configure --cluster $(CONFIG_NAME) --default-launch-type EC2 --config-name $(CONFIG_NAME) --region us-east-1
	ecs-cli configure profile --access-key $(AWS_ACCESS_KEY) --secret-key $(AWS_SECRET_KEY) --profile-name $(CONFIG_NAME)-profile
	ecs-cli up --keypair devSitePair --capability-iam --size 1 --instance-type t3a.medium --cluster-config $(CONFIG_NAME) --ecs-profile $(CONFIG_NAME)-profile --force

buildAWS:
	cd $(PROJECT_HOME)/aws && \
	docker-compose -f docker-compose.aws-build.yml build

pushAWS:
	aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $(AWS_ACCOUNT_ID).dkr.ecr.us-east-1.amazonaws.com
	cd $(PROJECT_HOME)/aws && \
	docker-compose -f $(PROJECT_HOME)/aws/docker-compose.aws-build.yml push 

publishBlogs:
	cd $(PROJECT_HOME)/devel/blog && \
	ls *.ipynb | nb2hugo --site-dir ./../blog --section posts


# deployAWS:
# 	cd $(PROJECT_HOME)/aws && \
# 	ecs-cli compose --project-name devSite service up --create-log-groups --cluster-config devSite --ecs-profile devSite-profile --timeout 20 \
# 		--target-group-arn $(TG_ARN) --container-port 80 --container-name traefik
awsUp:
	cd $(PROJECT_HOME)/aws && ecs-cli compose up --create-log-groups --cluster-config $(CONFIG_NAME) --ecs-profile $(CONFIG_NAME)-profile

awsDown:
	cd $(PROJECT_HOME)/aws && ecs-cli compose down --create-log-groups --cluster-config $(CONFIG_NAME) --ecs-profile $(CONFIG_NAME)-profile

awsPs: 
	ecs-cli ps --cluster-config $(CONFIG_NAME) --ecs-profile $(CONFIG_NAME)-profile	

build:
	docker-compose -f docker-compose.prod.yml build

push:
	docker-compose -f docker-compose.prod.yml push

copyEnv:
	scp .env* deployer@$(DROPLET_IP):/home/deployer/commute
	scp docker-compose* deployer@$(DROPLET_IP):/home/deployer/commute
	scp dockerservice/* deployer@$(DROPLET_IP):/home/deployer/commute/docker-service

deploy:
	docker-compose -f docker-compose.deploy.yml down -v
	docker rmi $(docker images -f "dangling=true" -q)
	docker volume prune
	docker-compose -f docker-compose.deploy.yml pull
	docker-compose -f docker-compose.deploy.yml up -d --force-recreate

