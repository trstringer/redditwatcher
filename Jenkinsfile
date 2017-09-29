pipeline {
  agent any
  environment {
    BUILD_VERSION = '$(python3 -c \'from version import VERSION; print(VERSION,end="")\')'
    DOCKER_REPOSITORY = 'trstringer/redditwatcher'
  }
  stages {
    stage('Build') {
      steps {
        echo "building..."
        sh "docker build -t ${env.DOCKER_REPOSITORY}:${env.BUILD_VERSION} ."
        sh "docker run --rm --env-file env --name rw ${env.DOCKER_REPOSITORY}:${env.BUILD_VERSION}"
      }
    }
    stage('Test') {
      steps {
        sh 'bash ./integration/integration_tests.sh'
      }
    }
    stage('Deliver') {
      when {
        expression {
          currentBuild.result == null || currentBuild.result == 'SUCCESS'
        }
      }
      steps {
        echo "pushing image to container registry..."
        sh "docker push ${env.DOCKER_REPOSITORY}:${env.BUILD_VERSION}"
      }
    }
  }
  post {
    always {
      sh "docker stop rw"
      sh "docker image prune -f"
    }
    failure {
      mail bcc: '', body: 'redditwatcher build failed', cc: '', from: '', replyTo: '', subject: '<redditwatcher> Build failed', to: 'github@trstringer.com'
    }
  }
}
