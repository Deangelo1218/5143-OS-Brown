def cat(**kwargs):

  params = kwargs['params']

  if not isinstance(params,list):
   params = [params]
  print(params)
  print("\n params[0] is "+params[0])
  for file in params:
    #print('\nfile')
    with open(file, "r") as f:
      lines = f.read().splitlines()
    print('\n')
    for line in lines:
      print(line)