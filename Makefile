buildPushAWS: buildAWS pushAWS

buildAWS:
	cd $(PROJECT_HOME)/aws && \
	docker-compose -f docker-compose.aws-build.yml build

pushAWS:
	aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $(AWS_ACCOUNT_ID).dkr.ecr.us-east-1.amazonaws.com
	cd $(PROJECT_HOME)/aws && \
	docker-compose -f $(PROJECT_HOME)/aws/docker-compose.aws-build.yml push 

# deployAWS:
# 	cd $(PROJECT_HOME)/aws && \
# 	ecs-cli compose --project-name devSite service up --create-log-groups --cluster-config devSite --ecs-profile devSite-profile --timeout 20 \
# 		--target-group-arn $(TG_ARN) --container-port 80 --container-name traefik
awsUp:
	cd $(PROJECT_HOME)/aws && ecs-cli compose up --create-log-groups --cluster-config devSite --ecs-profile devSite-profile

awsDown:
	cd $(PROJECT_HOME)/aws && ecs-cli compose down --create-log-groups --cluster-config devSite --ecs-profile devSite-profile

awsPs: 
	ecs-cli ps --cluster-config devSite --ecs-profile devSite-profile	
