// This statement loads shared library directly from git repo and no configuration for Jenkins is needed
// Stages actually use variables from shared library so it's easy to update a bunch of jobs at once.
library identifier: 'platform-shared-libs@master', retriever: modernSCM(
        [$class       : 'GitSCMSource',
         remote       : 'git@github.com:integralads/ds-platform-jenkinsng-utils.git',
         credentialsId: 'read-only-clone-ssh-key'])

// Add ddl scrips to ddlScripts map
// Format: XXXX-version--script_name.hql: irreversible flag, where XXXX - sequential number
// for example:
// '0000-1.0.1--tables_setup.hql': false,
// '0001-1.0.2--raw_table_data_and_metadata_cleanup.sh': true,
// '0002-1.0.2--tables_setup.hql': false,
ddl_scripts = [:]

Map settings = [
        pipeline_generator: global_pipeline_generator,
        // Line of Business to be used for deployment execution
        lob: '',
        additional_credentials: ['de-user'],
        approvers: [
                dev: 'automatic',
                staging: getFullTeamNames('Cloud9','Release Engineering','Tiger Kings'),
                prod: getFullTeamNames('Cloud9','Release Engineering','Tiger Kings')
        ],
        ddl_scripts: ddl_scripts
]

createTagOnMergeTo(branch: 'master')

pullRequestPipeline {

    // Build and Test on every commit
    buildAppAndConfig(settings)
    unitTest(settings)

    // Deploy to Airflow and S3 - only if triggered manually
    if(isManuallyTriggered()) {
        String environment = 'dev'
        settings = settings + [
                environment: environment,
                notify_slack: ''
        ]

        releaseToNexus(settings)
        deployToAirflowServer(settings)
        deployToS3(settings)
        launchDatalakeDDL(settings)
    }
}

tagReleasePipeline{
    String response = tagBuildChoices(settings)

    if (response == 'Deploy to Airflow Server + S3 in Staging'){
        String environment = 'staging'
        settings = settings + [
                environment: environment,
                notify_slack: ''
        ]
    } else if (response == 'Deploy to Airflow Server + S3 in Production'){
        String environment = 'prod'
        settings = settings + [
                environment: environment,
                notify_slack: ''
        ]
    }

    releaseToNexus(settings)
    deployToAirflowServer(settings)
    deployToS3(settings)
    launchDatalakeDDL(settings)
}

def unitTest(Map settings){
    stage('Unit Test'){
        buildAgent(settings) {
            try {
                echo 'Running Flake8 checks...'
                runToolChainsSh(settings, "sh ./.ci/all_tests.sh")
            } finally {
                //junit 'build/test-results/**/*.xml'
            }
        }
    }
}

String tagBuildChoices(Map settings){
    String response
    stage('Job Choices'){
        timeout(time: 15, unit: 'MINUTES') {
            response = input message: '', parameters: [
                    choice(
                            choices:[
                                    'Deploy to Airflow Server + S3 in Staging',
                                    'Deploy to Airflow Server + S3 in Production'
                            ],
                            description: 'Select Deployment Choices',
                            name: 'Job Choices'
                    )
            ]
        }
    }
    return response
}
