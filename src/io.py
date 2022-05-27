def loadWords(path):
  with(open(path, 'r')) as file:
      lines = file.readlines()
      return [x.strip() for x in lines]