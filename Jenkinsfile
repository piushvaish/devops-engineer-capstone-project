#!/usr/bin/groovy
import groovy.json.JsonOutput
//
pipeline {
    
  options {
      buildDiscarder(logRotator(numToKeepStr:'10'))
      timeout (time: 120, unit: 'MINUTES')
    } 
    stages {
      stage('DockerFile') {
            agent {
                dockerfile true
            }
            steps {
                sh 'node --version'
            }
        }
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
      stage('Build Docker Container') {
        agent {
          dockerfile true
        }
      		steps {
			    sh 'docker build -f Dockerfile . -t jupyter --label jupyter'
          sh 'docker run -it -p 8888:8888 jupyter'
            }
        }
      
      stage("Cleaning Docker up") {
        agent {
          dockerfile true
        }
                    steps {
                script {
                    sh "echo 'Cleaning Docker up'"
                    sh "docker system prune"
                }
            }
        }
      }
  }
