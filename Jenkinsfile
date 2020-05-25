#!/usr/bin/groovy
import groovy.json.JsonOutput
//
pipeline {
  options {
      buildDiscarder(logRotator(numToKeepStr:'10'))
      timeout (time: 120, unit: 'MINUTES')
    } 


  parameters {   
      string (name: 'BUCKET_NAME',
          description: "Choose BUCKET to run the job",
          defaultValue:'pv-capstone-project')      
      booleanParam (name: 'CREATE_REPORT',
            description: "This allows to test a dryrun  what files will be created based on configuration",
              defaultValue: true) 
      booleanParam (name: 'COPY_S3',
            description: "This allows to copy files to S3",
              defaultValue: true) 
    }
    
  agent any
    

stages {     
    stage ('CONFIGURE: Check Python Template  ') {
        when {
            expression { params.CREATE_REPORT == true }
        }
        steps {                
              script {
                def workspace = pwd()
                env.WORKSPACE = workspace
              sh """ 
              pwd
              python3 test1.py 
            
              """
                              
        }
    }

    }
    
    stage ('S3 COPY') {
        when {
            expression { params.COPY_S3 == true }
        }
        steps {
          
            retry(3) {
                withAWS(region:'us-west-2', credentials: 'aws-static') {
                    s3Upload(bucket:'pv-capstone-project' , includePathPattern:'**/*', excludePathPattern:'**/*.svg,**/*.jpg')
                }
            }
            
    }

  }
    
}   
}
