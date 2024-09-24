pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "ghcr.io/kolawatinpan/softdev"
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/KolawatInpan/softdev.git', branch: 'main', credentialsId: 'github-secret'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    def customImage = docker.build("${env.DOCKER_IMAGE}:${env.BUILD_ID}", ".")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([string(credentialsId: 'github-secret', variable: 'GITHUB_TOKEN')]) {
                    sh '''
                        echo $GITHUB_TOKEN | docker login ghcr.io -u KolawatInpan --password-stdin
                        docker push ${DOCKER_IMAGE}:${BUILD_ID}
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // Add your deployment steps here, e.g., using Docker Compose
                    sh 'docker compose down'
                    sh 'docker compose up -d'
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