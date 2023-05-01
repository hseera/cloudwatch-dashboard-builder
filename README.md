# CloudWatch Dashboard Builder ![Language Python](https://img.shields.io/badge/%20Language-python-blue.svg) [![Apache License](http://img.shields.io/badge/License-Apache-blue.png)](LICENSE) [![GitHub Last Commits](https://img.shields.io/github/last-commit/hseera/cloudwatch-dashboard-builder.svg)](https://github.com/hseera/cloudwatch-dashboard-builder/commits/) [![GitHub Size](https://img.shields.io/github/repo-size/hseera/cloudwatch-dashboard-builder.svg)](https://github.com/hseera/cloudwatch-dashboard-builder/) 

The CloudWatch Dashboard Builder is a useful and convenient tool for individuals such as Site Reliability Engineers (SREs), Performance Engineers, and DevOps professionals who work with AWS services. It enables the generation of the CloudWatch dashboard template from various AWS Namespaces. The metric query for different AWS namespaces can be in the SQL expression form too.

![Cloudwatch-dashboard-builder](https://user-images.githubusercontent.com/59352356/212447790-8891e0c1-a61f-4e62-8868-9aa28512c544.gif)

<!-- ![Alt text](/images/cloudwatch-dashboard.png?raw=true "CloudWatch Dashboard Builder")-->

## Table of contents
* [Background](#background)
* [Features](#features)
* [Requirements](#requirements)
* [How to use the code](#how-to-use-the-code)
* [Tool Caveats](#tool-caveats)
* [Future Enhancements](#future-enhancements)
* [Blog post](#blog-post)
* [Who is talking about the CloudWatch Dashboard Builder](#who-is-talking-about-the-cloudwatch-dashboard-builder)
* [Contributing](#contributing)
* [License](#license)


## [Background](#background)
I have been using the AWS CloudWatch service for close to 10 years for the purpose of monitoring and troubleshooting the performance of applications hosted on AWS. Throughout this period, I have devised various CloudWatch metric queries to facilitate the rapid creation of CloudWatch dashboards for various AWS services.

Initially, I would document commonly used metrics in a notepad, and refer to them as necessary when creating CloudWatch dashboards for new projects, clients, or applications. On occasions, I would not have access to CloudWatch, necessitating that I request a colleague to create a widget or dashboard. Prior to making such requests, it was necessary for me to convert the query into JSON format. Due to these factors and introduction of SQL expression for metrics, I developed a tool for constructing CloudWatch dashboards to improve my productivityby reducing the amount of time spent on repetitive tasks.

The CloudWatch Dashboard Builder grants the capability to generate a time series dashboard template from a selection of predefined metric queries that are included with the tool, or custom ones. Additionally, the dashboard can be created directly from the tool, or the JSON can be copied and the dashboard created through the console or CLI. This is a valuable tool for those who work in the realm of observability and utilize AWS services.

## [Features](#features)
- Customizable Namespace template
- Pre-build metric query templates for different AWS Namespaces
- Create CloudWatch dashboard directly from the tool
- List existing CloudWatch dashboards
- Dashboard template creation with a single click
- Capability to easily pick and choose AWS namespace metrics
- Automatically build widget layout (N x 2 widget layout)
- Time-series metric widgets only

## [Requirements](#requirements)
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

## [How to use the code](#how-to-use-the-code)
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
  
    Make sure you also set a default region.
    Set region in the AWS config file on your local system, located at:
    - ```~/.aws/config``` on Linux, macOS, or Unix.
    - ```C:\Users\USERNAME\.aws\config``` on Windows.

    This file should contain lines in the following format:
    ```
      [default]
      region = <YOUR_DEFAULT_REGION>
     ```
    Replace the value of ```<YOUR_DEFAULT_REGION>``` with your default AWS region. 
    ![image](https://user-images.githubusercontent.com/59352356/212446270-2a9d48b3-4454-4765-b228-7ddab70642a4.png)

  - Credential and region information in the tool
    Set AWS credentials in the tool with default region.
    ![image](https://user-images.githubusercontent.com/59352356/212445835-2619912b-3460-4770-89fe-b6bca13518b7.png)

- Run the code.
  For windows, the github repo already has an executable file that can be [downloaded](https://github.com/hseera/cloudwatch-dashboard-builder/blob/main/cloudwatch_dashboard_builder.zip) and executed. Otherwise run the application as follows:
  ```
  python cloudwatch-dashboard-builder.py
  ```
  On successful execution of the code, you will see the configuation screen.
  ![image](https://user-images.githubusercontent.com/59352356/212446672-a3869080-3109-4c1e-a372-329bc752698e.png)

  
## [Tool Caveats](#tool-caveats)
There are a couple of caveats that need to be taken into account.
- Currently there is only Windows executable shared on github.
- The present version produces only a time series dashboard.
- Double quotes in the namespace template queries need to be escaped.

## [Future Enhancements](#future-enhancements)
- Capability to select other types of graphs
- Capability to add Log Insights metrics
- Ability to build sql query expression within the tool
- Capability to save dashboard template for future use
- Ability to decide on the widget layout

## [Blog post](#blog-post)
- How to use CloudWatch Dashboard Builder [blog post](https://dev.to/aws-builders/aws-cloudwatch-dashboard-builder-tool-for-sre-performance-engineers-and-devops-29bi).

<!--Here is a video showing how to use it. https://user-images.githubusercontent.com/59352356/210024787-b0e2f0f7-c04b-4512-b9af-71005532feb0.mp4 -->

## [Who is talking about the CloudWatch Dashboard Builder](#who-is-talking-about-the-cloudwatch-dashboard-builder)
- [AWS Open Source newsletter](https://dev.to/aws/aws-open-source-newsletter-140-1ie8)
- [TestGuild newsletter](https://www.linkedin.com/pulse/openai-playwright-pipelines-future-more-joe-colantonio)
- [AWS Community Builder Series Event - 2023](https://builders-apj.virtual.awsevents.com/media/t/1_u1h4qexv/281518872)
- [Twitter talk](https://twitter.com/mlabouardy/status/1618307774718566408?t=2EPTSyaeR5d3eUR_8yQbEw&s=19)
## [Contributing](#contributing)
Your contributions are always welcome! 

## [License](#license)
The CloudWatch Dashboard Builder is an open-source and free software released under the [APACHE](https://github.com/hseera/cloudwatch-dashboard-builder/blob/main/LICENSE) (Apache License 2.0).


