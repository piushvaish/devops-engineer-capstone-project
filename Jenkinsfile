pipeline {
  options {
        buildDiscarder(logRotator(numToKeepStr:'10'))
        timeout (time: 120, unit: 'MINUTES')
        ansiColor('xterm')
    } 

    environment {       
          SUPPORT_GROUP = "ahavars@gmail.com"
          AWS_ACC_ID = sh(returnStdout:true, script: 'aws sts get-caller-identity --output text --query "Account"').trim()
          PV-DEVOPS = '8746-1031-5471'
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
 
    post {
               
        aborted {
            emailext (
                attachLog: true,
                subject: '[ABORTED] $PROJECT_NAME - BuildNumber:$BUILD_NUMBER',
                to: "${env.SUPPORT_GROUP}" ,
                replyTo: "${env.SUPPORT_GROUP}",
                body: '''You are receiving this email because Report was TRIGGERED.\n\nReview the build logs to know more about the build.\n\nBuild URL: ${BUILD_URL}'''
            )
        }
        unstable {
            emailext (
                attachLog: true,
                subject: '[UNSTABLE] $PROJECT_NAME - BuildNumber:$BUILD_NUMBER',
                to: "${env.SUPPORT_GROUP}",
                replyTo: "${env.SUPPORT_GROUP}",
                body: '''You are receiving this email because Report was TRIGGERED .\n\nReview the build logs to know more about the build.\n\nBuild URL: ${BUILD_URL}'''
            )
        }
        failure {
            emailext (
                attachLog: true,
                subject: '[FAILURE] $PROJECT_NAME - BuildNumber:$BUILD_NUMBER',
                to: "${env.SUPPORT_GROUP}",
                replyTo: "${env.SUPPORT_GROUP}",
                body: '''You are receiving this email because Report was TRIGGERED.\n\nReview the build logs to know more about the build.\n\nBuild URL: ${BUILD_URL}'''
            )

        }
        success {
            emailext (
                attachLog: true,
                subject: '[SUCCESS] $PROJECT_NAME - BuildNumber:$BUILD_NUMBER',
                to: "${env.SUPPORT_GROUP}",
                replyTo: "${env.SUPPORT_GROUP}",
                body: '''You are receiving this email because Report was TRIGGERED.\n\nReview the build logs to know more about the build.\n\nBuild URL: ${BUILD_URL}.'''
            )
        }

        always { 
            cleanWs()
         }
  
    } 

    
}
