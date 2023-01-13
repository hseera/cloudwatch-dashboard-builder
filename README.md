# CloudWatch Dashboard Builder
Generate a Cloudwatch Dashboard from Cloudwatch metrics (including sql queries).

![Alt text](/images/cloudwatch-dashboard.png?raw=true "CloudWatch Dashboard Builder")

For over five years, I have been using the AWS CloudWatch service for monitoring and troubleshooting application performance. Over that period, I have developed different Cloudwatch metric queries to help me quickly create CloudWatch dashboards or widgets for different AWS services.

In the beginning, I used to write these queries in a notepad. From time to time, I would refer them to create a CloudWatch dashboard or widget if I needed them for a new project, client, or application. I occasionally lacked access to CloudWatch, so I had to ask a colleague to create a widget or dashboard. Before requesting them, I had to transform the query into JSON format. These reasons led me to create a tool for building CloudWatch dashboards.

The CloudWatch Dashboard Builder tool allows you to create a time series dashboard template from various predefined metric queries or a custom ones. SQL expressions can be used in metric queries too. Also you can create the dashboard directly from the tool or copy the JSON and create it through the console/CLI. A useful tool to have if you work in Observability space and with AWS services.

https://user-images.githubusercontent.com/59352356/210024787-b0e2f0f7-c04b-4512-b9af-71005532feb0.mp4


To learn about how to use this tool, I have written a [blog post](https://dev.to/aws-builders/aws-cloudwatch-dashboard-builder-tool-for-sre-performance-engineers-and-devops-29bi)
