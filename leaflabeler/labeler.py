import os
import cPickle as pickle
import json

#class Label(object):
#    def __init__(self, post_dict):
#        self.post_dict = post_dict
        
class LeafLabeler(object):

    def __init__(self):
        print '\n\nStarting LeafLabeler.'
        self.image_dir = os.environ['leaflabeler_image_dir']
        self.image_list = os.environ['leaflabeler_image_list']
        self.label_output_file = os.environ['leaflabeler_label_output_file']

        print 'Arguments received:'
        print '  image_dir:', self.image_dir
        print '  image_list:', self.image_list
        print '  label_output_file:', self.label_output_file

        with open(self.image_list, 'r') as ff:
            self.images = [line.strip() for line in ff]

        self.n_images = len(self.images)
        print 'Read %d image filenames from %s' % (self.n_images, self.image_list)
        if self.n_images == 0:
            raise Exception('No images found in file %s!' % self.image_list)

        # Check that each files exists
        for im in self.images:
            impath = os.path.join(self.image_dir, im)
            print '  Checking:', impath
            if not os.path.exists(impath):
                raise Exception('File %s specified, but it does not exist! Check the image_dir (%s) and lines of the image_list (this line: %s) for problems' % (impath, self.image_dir, im))
        print 'Verified all %d files.' % len(self.images)
        
        self.labels = []
        self.next_ii = 0
        self.labeler_id = None

        print '\n'

    def get_stage(self):
        if self.labeler_id == None:
            return 'start'
        elif len(self.labels) == self.n_images:
            return 'done'
        else:
            return 'label'

        
    def get_next_image(self):
        if self.next_ii < self.n_images:
            imkey = self.next_ii
            #impath = os.path.join(self.image_dir, self.images[self.next_ii])
            imname = self.images[self.next_ii]
            #self.next_ii += 1
            return (imkey, imname)
        else:
            return None  # No images left

    def update_labeler_id(self, labeler_id):
        assert isinstance(labeler_id, int), 'expected int'
        self.labeler_id = labeler_id
        
    def update_label(self, posted_data):
        '''Expects labels to be updated in order'''
        
        results = json.loads(posted_data['results'])
        assert len(results.keys()) == 1, 'Expected a single image key'
        expected_key = len(self.labels)
        imkey = int(results.keys()[0])
        assert imkey >= 0 and imkey < self.n_images, 'completely bad key %s (allowed range 0 to %d)' % (imkey, self.n_images)
        assert imkey == expected_key, 'key out of order (got %d, expected %d)' % (imkey, expected_key)
        self.labels.append(posted_data)
        self.next_ii = imkey + 1

    def write_to_file(self):
        data_dict = {'version': 1,
                     'labeler_id': self.labeler_id,
                     'image_dir': self.image_dir,
                     'image_list': self.image_list,
                     'images': self.images,
                     'labels': self.labels}
                     
        with open(self.label_output_file, 'wb') as ff:
            pickle.dump(data_dict, ff, -1)
            
# Define a global leaflabeler object
#if not 'leaflabeler' in locals() or 'leaflabeler' in globals():
#    leaflabeler = LeafLabeler()

