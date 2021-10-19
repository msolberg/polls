#!/usr/bin/env groovy

def towerUrl = 'towerUrl'
def towerInventory = 'towerInventory'
def towerCredential = 'towerCredential'
def towerJobTemplate = 'towerJobTemplate'

pipeline {
    agent any
    stages {
        stage('preamble') {
            steps {
                script {
                    openshift.withCluster() {
                        openshift.withProject() {
                            echo "Using project: ${openshift.project()}"
                        }
                    }
                }
                checkout([$class: 'GitSCM', branches: [[name: '**']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[url: 'https://github.com/msolberg/polls.git']]])
            }
        }
        stage('Build Container Image') {
            steps {
                script {
                    openshift.withCluster() {
                        openshift.withProject( 'polls-dev' ) {
                            openshift.selector("bc", "appserver").startBuild("--follow=true")
                        }
                    }
                }
            }
        }
        stage('Deploy to Dev') {
            steps {
                ansibleTower(
                    towerServer: "${towerUrl}",
                    towerCredentialsId: '',
                    templateType: 'job',
                    jobTemplate: "${towerJobTemplate}",
                    towerLogLevel: 'full',
                    inventory: "${towerInventory}",
                    jobTags: '',
                    skipJobTags: '',
                    limit: '',
                    removeColor: false,
                    verbose: true,
                    credential: "${towerCredential}",
                    extraVars: '''---
project_name:  "polls-dev"
replica_count: 1''',
                    async: false
                )
            }
        }
        stage('Deploy to Test') {
            steps {
                ansibleTower(
                    towerServer: "${towerUrl}",
                    towerCredentialsId: '',
                    templateType: 'job',
                    jobTemplate: "${towerJobTemplate}",
                    towerLogLevel: 'full',
                    inventory: "${towerInventory}",
                    jobTags: '',
                    skipJobTags: '',
                    limit: '',
                    removeColor: false,
                    verbose: true,
                    credential: "${towerCredential}",
                    extraVars: '''---
project_name:  "polls-test"
replica_count: 2''',
                    async: false
                )
            }
        }
        stage('Submit Promotion Ticket') {
            steps {
                ansibleTower(
                    towerServer: "${towerUrl}",
                    towerCredentialsId: '',
                    templateType: 'job',
                    jobTemplate: "Submit Ticket",
                    towerLogLevel: 'full',
                    inventory: "${towerInventory}",
                    jobTags: '',
                    skipJobTags: '',
                    limit: '',
                    removeColor: false,
                    verbose: true,
                    credential: "${towerCredential}",
                    extraVars: "sn_short_description:  Please release build ${env.BUILD_TAG} of Polls to Production",
                    async: false
                )
            }
        }
    }
}

