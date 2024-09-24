pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "ghcr.io/kolawatinpan/softdev"
        VENV_PATH = "${WORKSPACE}/venv"
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
                    sh '''
                        docker build -t ${DOCKER_IMAGE}:${BUILD_ID} .
                        docker run -d -p 8081:5000 ${DOCKER_IMAGE}:${BUILD_ID}
                        docker ps
                    '''
                }
            }
        }

        stage('Unit Tests') {
            steps {
                script {
                    // Create and activate a virtual environment, then run unit tests using unittest and coverage
                    sh '''
                        python3 -m venv ${VENV_PATH}
                        . ${VENV_PATH}/bin/activate
                        pip install -r requirements.txt
                        coverage run -m unittest unit_test.py --verbose
                        coverage report -m
                        deactivate
                    '''
                }
            }
        }

        stage('Robot Tests') {
            steps {
                script {
                    // Clone the repository containing Robot Framework tests, create and activate a virtual environment, then run the tests
                    sh '''
                        git clone https://github.com/KolawatInpan/api-robot.git
                        cd api-robot
                        . ../venv/bin/activate
                        pip install robotframework
                        pip install robotframework-requests
                        robot test.robot
                    '''
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([string(credentialsId: 'github-token', variable: 'GITHUB_TOKEN')]) {
                    sh '''
                        echo $GITHUB_TOKEN | docker login ghcr.io -u kolawatinpan --password-stdin
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
                    sh 'docker stop $(docker ps -a -q)'
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