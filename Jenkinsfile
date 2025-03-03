pipeline {
    agent any

    environment {
        IMAGE_NAME = "flask-chat"        
        REGISTRY = "assesment-demo"    
        TAG = "latest"                     
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${REGISTRY}/${IMAGE_NAME}:${TAG} ."
                }
            }
        }

        stage('Deploy Application') {
            steps {
                script {
                    // Run the Docker container
                    sh """
                    docker stop ${IMAGE_NAME} || true
                    docker rm ${IMAGE_NAME} || true
                    docker run -d --name ${IMAGE_NAME} -p 8080:5000 ${REGISTRY}/${IMAGE_NAME}:${TAG}
                    """
                }
            }
        }
    }

    post {
        always {
            // Clean up unused images
            script {
                sh "docker image prune -f"
            }
        }
        success {
            echo 'Deployment completed successfully!'
        }
        failure {
            echo 'Deployment failed. Check the logs for errors.'
        }
    }
}
