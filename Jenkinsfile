pipeline {
     agent any
     stages {
         stage('Build') {
             steps {
                 sh 'echo "Hello World"'
                 sh '''
                     echo "Multiline shell steps works too"
                     ls -lah
                 '''
             }
         }
         stage('Upload to AWS') {
            steps {
                retry(3) {
                    withAWS(region:'us-west-2', credentials: 'aws-static') {
                        s3Upload(file:'sample_test.csv', bucket:'pv-capstone-project', path:'sample_test.csv')
                    }
                }
            }
        }
        stage('Health check') {
            steps {
                sh 'curl --silent --fail "http://pv-project3.s3-website-us-west-2.amazonaws.com/" >/dev/null'
            }
        }
        
    }
     }
}