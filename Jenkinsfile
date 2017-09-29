pipeline {
  agent any
  environment {
    BUILD_VERSION = '$(python3 -c \'from version import VERSION; print(VERSION,end="")\')'
    DOCKER_REPOSITORY = 'trstringer/redditwatcher'
  }
  stages {
    stage('Build') {
      environment {
        REDDITWATCHER_CLIENTID = credentials('REDDITWATCHER_CLIENTID')
        REDDITWATCHER_CLIENTSECRET = credentials('REDDITWATCHER_CLIENTSECRET')
      }
      steps {
        echo "building..."
        sh "docker build -t ${env.DOCKER_REPOSITORY}:${env.BUILD_VERSION} ."
        sh "docker run --rm -e REDDITWATCHER_CLIENTID=${env.REDDITWATCHER_CLIENTID} -e REDDITWATCHER_CLIENTSECRET=${env.REDDITWATCHER_CLIENTSECRET} --name rw ${env.DOCKER_REPOSITORY}:${env.BUILD_VERSION} linux"
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
