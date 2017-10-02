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
        sh "docker build -t ${env.DOCKER_REPOSITORY}:${env.BUILD_VERSION} -t ${env.DOCKER_REPOSITORY}:latest ."
        sh "docker run -d -e REDDITWATCHER_CLIENTID=${env.REDDITWATCHER_CLIENTID} -e REDDITWATCHER_CLIENTSECRET=${env.REDDITWATCHER_CLIENTSECRET} --name rw ${env.DOCKER_REPOSITORY}:${env.BUILD_VERSION} linux"
      }
    }
    stage('Test') {
      steps {
        sh "sleep 2"
        sh "docker logs rw"
        sh "docker ps | grep rw"
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
      sh "docker stop rw || true"
      sh "docker rm rw || true"
      sh "docker image prune -f"
    }
    failure {
      mail bcc: '', body: 'redditwatcher build failed', cc: '', from: '', replyTo: '', subject: '<redditwatcher> Build failed', to: 'github@trstringer.com'
    }
  }
}
