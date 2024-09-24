pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "ghcr.io/KolawatInpan/softdev"
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/KolawatInpan/softdev.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${env.DOCKER_IMAGE}:${env.BUILD_ID}")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://ghcr.io', 'github_credentials') {
                        docker.image("${env.DOCKER_IMAGE}:${env.BUILD_ID}").push()
                        docker.image("${env.DOCKER_IMAGE}:${env.BUILD_ID}").push('latest')
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // Add your deployment steps here, e.g., using Docker Compose
                    sh 'docker-compose down'
                    sh 'docker-compose up -d'
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}