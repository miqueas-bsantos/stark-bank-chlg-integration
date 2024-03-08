import sys, os
from os import environ

environ['STAGE'] = 'development'
environ['TEST'] = 'TRUE'

# Linux
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path + "/../")

# Windows
# testPath = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0, testPath)
# sys.path.insert(0, testPath + '\\..\\src\\')

os.environ['TZ'] = 'America/Sao_Paulo'
os.environ['REGION'] = 'us-east-1'
os.environ['ACCOUNT'] = '00000000'
os.environ['AWS_DEFAULT_REGION'] = os.environ['REGION']
