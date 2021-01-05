# Cleanup Lambda Function

This folder contains a Lambda function, deployed via [SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html), that searches for orphaned EC2 instances created by Molecule via the projects Travis build. This is typically caused by failed or cancelled builds that do not get a chance to cleanup their resources.

The lambda function is triggered once per day via CloudWatch.

## Prerequisites

* [Python 3 installed](https://www.python.org/downloads/)
* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)

## Deploy

To build and deploy your application for the first time, run the following in your shell:

```bash
sam build
sam deploy --guided
```

The first command will build the source of your application. The second command will package and deploy your application to AWS, with a series of prompts:

* **Stack Name**: The name of the stack to deploy to CloudFormation. This should be unique to your account and region, and a good starting point would be something matching your project name.
* **AWS Region**: The AWS region you want to deploy your app to.
* **Confirm changes before deploy**: If set to yes, any change sets will be shown to you before execution for manual review. If set to no, the AWS SAM CLI will automatically deploy application changes.
* **Allow SAM CLI IAM role creation**: Many AWS SAM templates create AWS IAM roles required for the AWS Lambda function(s) included to access AWS services. By default, these are scoped down to minimum required permissions. To deploy an AWS CloudFormation stack which creates or modified IAM roles, the `CAPABILITY_IAM` value for `capabilities` must be provided. If permission isn't provided through this prompt, to deploy this example you must explicitly pass `--capabilities CAPABILITY_IAM` to the `sam deploy` command.
* **Save arguments to samconfig.toml**: If set to yes, your choices will be saved to a configuration file inside the project, so that in the future you can just re-run `sam deploy` without parameters to deploy changes to your application.

## Cleanup

To delete the application that you created, use the AWS CLI. Assuming you used "CleanupLambda" for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name CleanupLambda
```
