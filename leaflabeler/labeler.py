import os

class LeafLabeler(object):

    def __init__(self):
        print 'LeafLabeler: Grabbing arguments from environment'
        self.infile = os.environ['leaflabeler_infile']
        self.outfile = os.environ['leaflabeler_outfile']

        print 'initialized', self.infile, self.outfile



# Define a global leaflabeler object
if not 'leaflabeler' in locals() or 'leaflabeler' in globals():
    leaflabeler = LeafLabeler()

