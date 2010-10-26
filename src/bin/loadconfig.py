def load_config():
    from ConfigParser import ConfigParser
    import os
    parser = ConfigParser()
    parser.read(os.path.join(os.path.curdir, "vmxray.conf"))
    y = dict(parser.items('DIRECTORIES'))
    for x in y.keys():
        y[x] = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', y[x]))
    return y 
conf = load_config()
