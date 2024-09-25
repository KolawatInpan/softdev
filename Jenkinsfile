pipeline {
    // agent { label 'vm1'}
    agent any

    environment {
        APP_NAME = "app"
        DOCKER_IMAGE = "ghcr.io/kolawatinpan/softdev"

        ROBOT_REPO = "https://github.com/KolawatInpan/api-robot.git"
        ROBOT_BRANCH = "main"
        ROBOT_FILE = "test.robot"

        MAIN_REPO = "https://github.com/KolawatInpan/softdev.git"
        MAIN_BRANCH = "main"

        GITHUB_TOKEN = credentials('github-token')
        GITHUB_SECRET = 'github-secret'

        VENV_PATH = "${WORKSPACE}/venv"
    }

    stages {
        stage('Checkout') {
            steps {
                git url: "${MAIN_REPO}", branch: "${MAIN_BRANCH}", credentialsId: "${GITHUB_SECRET}"
            }
        }

        stage('Delete olds') {
            steps {
                script {
                    sh '''
                        docker stop \$(docker ps -a -q) || true
                        docker rm \$(docker ps -a -q) || true
                        docker rmi -f ${DOCKER_IMAGE}:${BUILD_ID} || true
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh '''
                        docker build -t ${DOCKER_IMAGE} .
                        docker run -d --name ${APP_NAME} ${DOCKER_IMAGE}
                        docker image ls
                        docker ps
                    '''
                }
            }
        }

        stage('Run Robot Tests') {
            steps {
                script {
                    sh '''
                        docker exec ${APP_NAME} robot ${ROBOT_FILE}
                    '''
                }
            }
        }

        stage('Unit Tests') {
            steps {
                script {
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
            // agent { label 'vm3'}
            steps {
                script {
                    sh '''
                        docker login ghcr.io -u kolawatinpan -p $GITHUB_TOKEN
                        docker pull ${DOCKER_IMAGE}:${BUILD_ID}
                        docker run -d -p 5000:5000 --name ${APP_NAME} ${DOCKER_IMAGE}:${BUILD_ID}
                    '''
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