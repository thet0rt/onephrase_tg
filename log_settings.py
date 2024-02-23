import logging
log = logging.getLogger('logger')
log.setLevel(logging.DEBUG)
fh = logging.FileHandler('app.log', 'a', 'utf-8')
formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(message)s')
fh.setFormatter(formatter)
log.addHandler(fh)
