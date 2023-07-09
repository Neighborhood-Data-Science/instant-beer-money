First, we need to download the CLI for both Docker and AWS.
Once this is downloaded, we need to configure our AWS SSO login to utilize the AWS CLI.
In your terminal, execute the following code to begin set up:

`aws configure sso`

Once your AWS CLI is configured properly, you must autheticate your Docker CLI to your default Amazon ECR.
Note that the <profile_name> is required and is setup using the previous `aws configure sso` command.
In your terminal, execute the following code:

aws ecr get-login-password \                                                                    
    --region <aws_account_region> --profile <profile_name> \
| docker login \
    --username AWS \
    --password-stdin <aws_account_id>.dkr.ecr.<region>.amazonaws.com/<aws_repo_name>

You should now be authenticated.
Now, cd to the directory containing your Dockerfile then build the Docker image
NOTE: I'm using 'buildx' command to build properly on Apple Silicon (M2)

docker buildx build -t <docker_image_name>:<docker_image_tag> .   

You may occasionally need to use the --no-cache flag to do a clean build.
docker buildx build --no-cache -t <docker_username>/<docker_image_name>:<docker_image_tag> .

Tag the image to be able to push to your Amazon ECR
docker tag <docker_image_name>:<docker_image_tag> <aws_account_id>.dkr.ecr.<region>.amazonaws.com/<aws_repo_name>:<tag_name>

Push the image to your Amazon ECR
docker push <aws_account_id>.dkr.ecr.<region>.amazonaws.com/<aws_repo_name>:<tag_name>    
