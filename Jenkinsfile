pipeline {
    agent any
    environment {
        AWS_REGION = 'us-east-1'
        EKS_CLUSTER_NAME = 'your-eks-cluster'
        ECR_REPO_URI = '123456.dkr.ecr.${AWS_REGION}.amazonaws.com/flask-app'
        IMAGE_TAG="1.0"
    }
    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/your-repo/flask-app.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t flask-app .'
                    sh "docker tag flask-app:${IMAGE_TAG} ${ECR_REPO_URI}:${IMAGE_TAG}"
                }
            }
        }
        stage('Push to ECR') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-credentials']]) {
                    script {
                        sh '''
                        aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REPO_URI}
                        docker push ${ECR_REPO_URI}:latest
                        '''
                    }
                }
            }
        }
        stage('Update Image in Manifest') {
            steps {
                script {
                    sh '''
                    IMAGE_URI="${ECR_REPO_URI}:${IMAGE_TAG}"
                    sed -i "s|REPLACE_IMAGE|${IMAGE_URI}|g" deployment.yaml
                    '''
                }
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-credentials']]) {
                    script {
                        sh '''
                        aws eks --region ${AWS_REGION} update-kubeconfig --name ${EKS_CLUSTER_NAME}
                        kubectl apply -f deployment.yaml
                        kubectl apply -f service.yaml
                        '''
                    }
                }
            }
        }
    }
    post {
        success {
            echo 'Deployment Successful!'
        }
        failure {
            echo 'Deployment Failed!'
        }
    }
}
