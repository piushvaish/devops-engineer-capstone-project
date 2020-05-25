#!/usr/bin/groovy
import groovy.json.JsonOutput
//
pipeline {
  options {
        buildDiscarder(logRotator(numToKeepStr:'10'))
        timeout (time: 120, unit: 'MINUTES')
    } 

    environment {       
          SUPPORT_GROUP = "ahavars@gmail.com"
          AWS_ACC_ID = sh(returnStdout:true, script: 'aws sts get-caller-identity --output text --query "Account"').trim()
    }

    parameters {   
      /*  choice (name: 'PREFIX',
                description: "Choose what prefix the files 5o be deleted will have to run the job",
                choices:'pro\nstg\ndevqa') */
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
    
    agent {
        node {
            label "master"
        }    
    }
    /*
    triggers {
        cron('55 09 * * *')
        }
   
    */    

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
                
                  script {
                 sh """
                 
                aws s3 cp *.csv s3://$BUCKET_NAME --acl bucket-owner-full-control
                 """

            }
        }

       }
    
}

always { 
            cleanWs()
         }
  
    } 

    
}
