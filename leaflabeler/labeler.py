import os
import cPickle as pickle
import json

#class Label(object):
#    def __init__(self, post_dict):
#        self.post_dict = post_dict
        
class LeafLabeler(object):

    def __init__(self):
        print 'LeafLabeler: Grabbing arguments from environment'
        self.image_dir = os.environ['leaflabeler_image_dir']
        self.image_list = os.environ['leaflabeler_image_list']
        self.label_output_file = os.environ['leaflabeler_label_output_file']

        print 'initialized', self.image_dir, self.image_list, self.label_output_file

        with open(self.image_list, 'r') as ff:
            self.images = [line.strip() for line in ff]

        print 'got files', self.images
        # Check that each files exists

        self.n_images = len(self.images)
        if self.n_images == 0:
            raise Exception('No images found in file %s!' % self.image_list)

        self.labels = [None] * self.n_images
            
        for im in self.images:
            impath = os.path.join(self.image_dir, im)
            print impath
            if not os.path.exists(impath):
                raise Exception('File %s specified, but it does not exist! Check the image_dir (%s) and lines of the image_list (this line: %s) for problems' % (impath, self.image_dir, im))
        print 'Verified all %d files.' % len(self.images)
        
        self.next_ii = 0

    def get_next_image(self):
        if self.next_ii < self.n_images:
            imkey = self.next_ii
            #impath = os.path.join(self.image_dir, self.images[self.next_ii])
            imname = self.images[self.next_ii]
            #self.next_ii += 1
            return (imkey, imname)
        else:
            return None  # No images left

    def update_label(self, posted_data):
        results = json.loads(posted_data['results'])
        assert len(results.keys()) == 1, 'Expected a single image key'
        imkey = int(results.keys()[0])
        assert imkey >= 0 and imkey < self.n_images, 'bad key %s' % imkey
        self.labels[imkey] = posted_data
        self.next_ii = imkey + 1

    def write_to_file(self):
        data_dict = {'image_dir': self.image_dir,
                     'image_list': self.image_list,
                     'images': self.images,
                     'labels': self.labels}
                     
        with open(self.label_output_file, 'wb') as ff:
            pickle.dump(data_dict, ff, -1)
            
# Define a global leaflabeler object
#if not 'leaflabeler' in locals() or 'leaflabeler' in globals():
#    leaflabeler = LeafLabeler()

