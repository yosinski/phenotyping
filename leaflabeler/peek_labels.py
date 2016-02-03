#! /usr/bin/env python2.7

import os
import sys
import argparse
import textwrap
import pprint
import pickle



def main():
    parser = argparse.ArgumentParser(description='Peek at collected labels in a label pickle file')
    parser.add_argument('--all', action = 'store_true', help = 'Filename to read labels from.')
    parser.add_argument('label_file', type = str, help = 'Filename to read labels from.')
    args = parser.parse_args()

    with open(args.label_file, 'r') as ff:
        data = pickle.load(ff)

    print 'File %s content summary:' % args.label_file
    #print data

    print '  version:                   ', data['version']
    print '  image directory used:      ', data['image_dir']
    print '  image list used:           ', data['image_list']
    print '  number of images:          ', len(data['images'])
    print '    first image filename:    ', 'N/A' if len(data['images']) == 0 else data['images'][0]
    print '  number of labels collected:', len(data['labels'])
    toprint = 'None' if len(data['labels']) == 0 else repr(data['labels'][0])
    indent_len = 30
    toprint_pretty = textwrap.fill(toprint, 100,
                                   initial_indent = ' '*indent_len,
                                   subsequent_indent = ' '*indent_len)[indent_len:]
    print '    first label:             ', toprint_pretty

    if args.all:
        print '\ncomplete data from file follows:\n'
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(data)
        print



if __name__ == "__main__":
    main()
