import os

'''
setear SLACK_HOOK y BASE_URL como variables de entorno

export BASE_URL=http://url-de-my-api
export SLACK_HOOK=https://mytokendeslack

'''
SLACK_HOOK = os.getenv('SLACK_HOOK')
BASE_URL = os.getenv('BASE_URL')
