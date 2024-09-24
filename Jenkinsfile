pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "ghcr.io/kolawatinpan/softdev"
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/KolawatInpan/softdev.git', branch: 'main', credentialsId: 'github-admin'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${env.DOCKER_IMAGE}:${env.BUILD_ID}", ".")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://ghcr.io', 'github-admin') {
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