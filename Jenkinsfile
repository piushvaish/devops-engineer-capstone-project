#!/usr/bin/groovy
import groovy.json.JsonOutput
//
pipeline {
  options {
      buildDiscarder(logRotator(numToKeepStr:'10'))
      timeout (time: 120, unit: 'MINUTES')
    } 


  agent { dockerfile true }
    stages {
        stage('Test') {
            steps {
                sh 'node --version'
            }
        }
    }
}