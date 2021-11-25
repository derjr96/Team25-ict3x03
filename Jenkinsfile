pipeline {

    agent any

    environment { 
        CI = 'true'
    }

    stages {
        stage('Build') {
			steps {
				script {
					echo '-------- Performing Build Stage --------'
					try {
						sh 'python3 -m pipenv install Pipfile'
						sh 'python3 -m pipenv run python3 djangotaurus/manage.py collectstatic --noinput'
                        echo "Build has no errors! Proceeding on!"
                    } catch (Exception e) {
                        echo "Build has errors! Please check and verify!"
                    }
                }
            }
		}
		// TAKE NOTE:
		// RUN THIS ONLY IN THE EVENT OF DOCKER SERVICE RESTART AS GOOGLE CHROME IS IN THE CONTAINER ALREADY. JUST NEED TO RUN ONCE!

        // stage('Setup Chrome') {
        //     steps {
        //         echo '-------- Performing Chrome Setup Stage --------'
        //         sh 'apt update'
        //         sh 'apt --fix-broken -y install'
        //         sh 'apt install wget'
        //         sh 'apt-get install -fy gconf-service libasound2 libatk1.0-0 libcairo2 libcups2 libfontconfig1 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libxss1 fonts-liberation libnss3 lsb-release xdg-utils'
        //         sh 'wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb'
        //         sh 'dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install'
        //     }
        // }
        stage('Unit Test') {
            steps {
                script {
                    echo '-------- Performing Automated Unit Test Stage --------'
                    sh 'python3 -m pipenv run python3 djangotaurus/manage.py test djangotaurus.tests.test_transaction --keepdb'
                    sh 'python3 -m pipenv run python3 djangotaurus/manage.py test djangotaurus.tests.test_urls --keepdb'
                    sh 'python3 -m pipenv run python3 djangotaurus/manage.py test djangotaurus.tests.test_user --keepdb'
                    echo "Automated Unit Testing has no errors! Proceeding on!"
                }
            }
        }
        stage('Headless Browser Test') {
            steps {
                // Switch from production keys to test keys
                // Activation of Headless Script to allow captcha to run test keys
                echo '-------- Changing from production ReCAPTCHA keys to test ones  --------'
                dir("/home") {
                        sh "chmod +x headless.sh"
                        sh "./headless.sh"
                }
                echo '-------- Performing Headless Browser Test Stage --------'
                sh 'python3 -m pipenv run python3 djangotaurus/manage.py test djangotaurus.tests.test_register --keepdb'
                sh 'python3 -m pipenv run python3 djangotaurus/manage.py test djangotaurus.tests.test_login --keepdb'
                echo "Headless Browser Testing has no errors! Proceeding on!"
            }
        }
        stage('SonarQube Analysis') {
            steps {
                script {
                    echo '-------- Performing SonarQube Scan --------'
                    def scannerHome = tool 'ict3x03_Taurus_SonarQube_Scanner';
                    withSonarQubeEnv('SonarQube') {
                        sh "${scannerHome}/bin/sonar-scanner"
                    }
                       echo "SonarQube Analysis has no errors! Proceeding on!"
                }
            }
        }
        stage('OWASP Dependency Check') {
			steps {
			    echo '-------- Performing OWASP Dependency Check --------'
				dependencyCheck additionalArguments: '--disableYarnAudit --format HTML --format XML', odcInstallation: 'Default'
				dependencyCheckPublisher pattern: 'dependency-check-report.xml'
                echo "OWASP DependencyCheck has no errors! Proceeding on!"
			}
		}
        stage('Deploy') {
			steps {
				script {
					echo '-------- Performing Server Deployment --------'

					// Activation of Main Script to allow captcha to run production keys
                    // Switch back from test keys to production keys
                    echo '-------- Changing from test ReCAPTCHA keys to production ones  --------'
                    dir("/home") {
                        sh "chmod +x main.sh"
                        sh "./main.sh"
                    }

					try {
						sh 'kill -KILL $(lsof -t -i tcp:8082)'
						echo "There are uWSGI service and ports that are killed"
					} catch (Exception e) {
						echo "There is no uWSGI service to kill"
					}

					sh 'export JENKINS_NODE_COOKIE=dontKillMe'
					sh 'python3 -m pipenv run uwsgi --ini /home/Team25-AY21/uwsgi_djangotaurus.ini'
				}
			}		
        }
    }
}