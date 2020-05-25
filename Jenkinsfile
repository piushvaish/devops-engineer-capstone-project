#!/usr/bin/groovy
import groovy.json.JsonOutput
//
pipeline {
    
  options {
      buildDiscarder(logRotator(numToKeepStr:'10'))
      timeout (time: 120, unit: 'MINUTES')
    } 
    agent none
    stages {
      
    stage('Lint Dockerfile') {
      agent {
            docker {image 'hadolint/hadolint:latest-debian' }
            }
      steps {
            sh 'hadolint ./Dockerfile | tee -a hadolint_lint.txt'
            sh '''
                lintErrors=$(stat --printf="%s"  hadolint_lint.txt)
                if [ "$lintErrors" -gt "0" ]; then
                    echo "Errors have been found, please see below"
                    cat hadolint_lint.txt
                    exit 1
                else
                    echo "There are no erros found on Dockerfile!!"
                fi
            '''
              }
          }
    stage('Build DockerFile') {
          agent {
              dockerfile true
          }
          steps {
              sh 'node --version'
          }
      }
      stage('Scan Dockerfile to find vulnerabilities') {
            steps{
                aquaMicroscanner imageName: "piushvaish/capstone-project-jupyter:latest", notCompliesCmd: 'exit 4', onDisallowed: 'fail', outputFormat: 'html'
            }
        }
            
    }
}
