pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git 'https://github.com/Renuunaidu/case-monitoring-devops.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t case-monitoring .'
            }
        }

    }
}