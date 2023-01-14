# CloudWatch Dashboard Builder
Generate a time-series Cloudwatch Dashboard template from Cloudwatch metrics (including sql expressions).

![Alt text](/images/cloudwatch-dashboard.png?raw=true "CloudWatch Dashboard Builder")

# Background
For over five years, I have been using the AWS CloudWatch service for monitoring and troubleshooting application performance. Over that period, I have developed different Cloudwatch metric queries to help me quickly create CloudWatch dashboards or widgets for different AWS services.

In the beginning, I used to write these queries in a notepad. From time to time, I would refer them to create a CloudWatch dashboard or widget if I needed them for a new project, client, or application. I occasionally lacked access to CloudWatch, so I had to ask a colleague to create a widget or dashboard. Before requesting them, I had to transform the query into JSON format. These reasons led me to create a tool for building CloudWatch dashboards.

The CloudWatch Dashboard Builder gives you the capability to generate a time series dashboard template from various predefined metric queries that come with the tool or a custom ones. SQL expressions can be used in metric queries too. Also you can create the dashboard directly from the tool or copy the JSON and create it through the console/CLI. A useful tool to have if you work in Observability space and with AWS services.



## Requirements
- You must have an [Amazon Web Services (AWS) account](https://aws.amazon.com/).
- The code was written for:
  - Python 3
  - AWS SDK for Python (Boto3)
- Install the AWS SDK for Python (Boto3).
- Install the latest Boto 3 release via pip:
  ```
  pip install boto3
  ```
- Install the latest PySimpleGUi release via pip:
  ```
  pip install PySimpleGUI
  ```

## How to use the code
- Configure your AWS access keys.

  **Important:** For security, it is strongly recommend that you use IAM users instead of the root account for AWS access.

  When you initialize a new service client without supplying any arguments, the AWS SDK for Python attempts to find AWS credentials by using the default
  credential provider chain.

  Setting your credentials for use by the AWS SDK for Python can be done in a number of ways, but here are the recommended approaches:
  - The default credential profiles file.
  Set credentials in the AWS credentials profile file on your local system, located at:
    - ```~/.aws/credentials``` on Linux, macOS, or Unix.
    - ```C:\Users\USERNAME\.aws\credentials``` on Windows.

  This file should contain lines in the following format:
  ```
    [default]
    aws_access_key_id = <YOUR_ACCESS_KEY_ID>
    aws_secret_access_key = <YOUR_SECRET_ACCESS_KEY>
   ```
  Replace the values of ```<YOUR_ACCESS_KEY_ID>``` and ```<YOUR_SECRET_ACCESS_KEY>``` by your AWS credentials. 
  
  ![image](https://user-images.githubusercontent.com/59352356/212445731-3dcef972-1f75-4437-85eb-6bb088a3d32c.png)
- Credential information in the tool
  Set AWS credentials in the tool with default region.
  ![image](https://user-images.githubusercontent.com/59352356/212445835-2619912b-3460-4770-89fe-b6bca13518b7.png)


## Tool Caveats
There are a couple of caveats that need to be taken into account.
- Currently there is only Windows executable shared on github.
- The present version produces only a time series dashboard.
- Double quotes in the namespace template queries need to be escaped.

## Future Enhancements
- Capability to select other types of graphs
- Capability to add Log Insights metrics
- Extend the tool to Azure and Google Cloud
- Ability to build metric query within the tool

## Tool In Action & Blog post
Here is a video showing how to use it. Also there is a [blog post](https://dev.to/aws-builders/aws-cloudwatch-dashboard-builder-tool-for-sre-performance-engineers-and-devops-29bi) on how to use the tool.

https://user-images.githubusercontent.com/59352356/210024787-b0e2f0f7-c04b-4512-b9af-71005532feb0.mp4



