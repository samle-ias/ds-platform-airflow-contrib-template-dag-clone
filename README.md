# Common - Airflow DAG Initial Template with CICD Jenkins NG and Basic EMR Steps

## How-to Start

1. Use this repo as a Template (Clone or [__Use this template__](https://github.com/integralads/ds-platform-airflow-contrib-template-dag/generate) button)
2. Give _Read_ rights to _jenkins-ninja-ro-ias_ Github user
3. Applicable only to NON-FRAUD Repos: Give _Read_ rights to _PI Teams_ Github group
4. Give _Write_ rights to Contributing team's Github groups
5. Give _Admin_ rights to _RE Admin_ Github group, and users who need admin privileges (Example: team manager)
6. Update as part of first PR (if needed): Common Use Cases of Configurations for project customization
* Line of Business for deployment: [Update in cicd_aws_Jenkinsfile](https://github.com/integralads/ds-platform-airflow-contrib-template-dag/blob/master/.ci/cicd_aws_Jenkinsfile.groovy#L19)
* List of approvers for deployment: [Update in cicd_aws_Jenkinsfile](https://github.com/integralads/ds-platform-airflow-contrib-template-dag/blob/master/.ci/cicd_aws_Jenkinsfile.groovy#L23-L24)
* List of slack channels to get notified of deployment: Search for `notify_slack` in [cicd_aws_Jenkinsfile](https://github.com/integralads/ds-platform-airflow-contrib-template-dag/blob/master/.ci/cicd_aws_Jenkinsfile.groovy)
* DAG Name and AWS Tag: [Update in base airflow config](https://github.com/integralads/ds-platform-airflow-contrib-template-dag/blob/master/config/base.yaml#L13-L14)
* Product Name (your team's line of business): [Update in base airflow config](https://github.com/integralads/ds-platform-airflow-contrib-template-dag/blob/master/config/base.yaml#L16)
* Replace Nexus Group: [Update in gradle props](https://github.com/integralads/ds-platform-airflow-contrib-template-dag/blob/master/gradle.properties#L6)
7. After you are done editing dag/application name, on-board your repository to Jenkins NG ([read more](https://github.com/integralads/re-documentation/blob/master/jenkins-ng/getting-started.md#declaring-projects-for-your-team)) via PR of changes to [projects.yaml](https://github.com/integralads/jenkins-pipeline-scripts/blob/master/resources/com/integralads/projects.yml) (Add repo in your team's section maintaining alphabetical order)
8. After your PR was merged use [Generate Jenkins Jobs from YAML](https://jenkins.303net.net/job/_jervis_generator/build?delay=0sec) to add your Project to Jenkins-NG Web-UI
9. Go to your project sub-folder at [Jenkins-NG](https://jenkins.303net.net/view/GitHub%20Organizations/) (Example: [fraud](https://jenkins.303net.net/view/GitHub%20Organizations/job/fraud/)) and check out your application folder with the name your registered it in the step #6

## PR Branch Naming Conventions
* The branch name should correspond a Jira ticket which developer, for instance, `DF-1`
* PR Name should follow a pattern: `[Jira Ticket Number]: -Your PR description-`, for instance, `DF-1: Updates in CICD`

## Deploying to DEV from PR
1. Go to your application folder at [Jenkins-NG](https://jenkins.303net.net/view/GitHub%20Organizations/) and select `Pull Requests` tab. You should see your PR branch
2. Once `push` build succeeds you can build and deploy your code to AWS Airflow infrastructure by clicking `Build Now` in your PR page
3. Once the build succeeds go to [Common Airflow Dev Cluster Web UI](http://airflow-de-common.dev.303net.net:8080/admin/) and check out your pipeline. The pipeline name has `-v1-dev` as suffix. **Do not enable your Dag till you are done with the next step**
4. This template uses EMR to run and requires EMR Roles to execute pipeline, successfully. Go to your team's aws infrastructure repo and follow the instruction to create your pipeline CDK stack
5. Now everything is prepared for the predefined dag tasks to succeed. Go to [Common Airflow Dev Cluster Web UI](http://airflow-de-common.dev.303net.net:8080/admin/) and enable your Dag
6. (optional) In your application folder at [Jenkins-NG](https://jenkins.303net.net/view/GitHub%20Organizations/) push _Scan repository now_ -- all branches registered in the repo and mentioned in .jervis.yaml should appear on Jenkins-NG.

## Deploying to STAGING/PROD via TAG Builds
1. Once your PR is approved, the Jenkins Job will create a new TAG.
2. Once you see a new tag in Jenkins NG Project, click on new tag and then click `Build Now` to deploy either to Staging/Prod.

_To start use this Template press_ [__Use this template__](https://github.com/integralads/ds-platform-airflow-contrib-template-dag/generate) button.
After you follow above steps, continue building up your dag by adding more application code in `config` and `pipeline` folders.

