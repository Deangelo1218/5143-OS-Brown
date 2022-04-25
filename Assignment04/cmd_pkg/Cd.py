import os
from os.path import expanduser

def cd(**kwargs):
  params = kwargs.get("params", None)
  params = params[0]
  if '~' in params:
    params = params.replace('~', expanduser('~'))
    os.chdir(params)
      
  elif ' ' in params:
    params = params.replace(' ', expanduser(' '))
    os.chdir(params)
    
  elif '..' in params:
    os.chdir(os.path.dirname(os.getcwd()))
      
  elif params:
    os.chdir(params)
  return('in ' + os.getcwd())



if __name__ == "__main__":
  cd(params = "/home/runner/WonderfulSpotlessRecords/GeeksForGeeks")