#! /usr/bin/env python2.7

import os
import sys
import argparse



def main():
    # Note: main sometimes runs multiple times as a result of
    # execute_from_command_line trickery. This should be fine though.

    parser = argparse.ArgumentParser(description='Main script for running LeafLabeler')
    parser.add_argument('image_dir', type = str,
                        help = 'Path to directory containing images (relative or absolute path)')
    parser.add_argument('image_list', type = str, help = 'List of image files to label this time.')
    parser.add_argument('label_output_file', type = str, help = 'Filename to write labels to.')
    args = parser.parse_args()

    proj_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'opensurfaces-segmentation-ui',
                            'example_project')
    #print 'inserting', proj_dir
    sys.path.insert(0, proj_dir)
    #print sys.path
                    
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "example_project.settings")

    # Export to environ for loading in LeafLabeler object (messy, but
    # easiest way to pass info from here into class)
    os.environ['leaflabeler_image_dir'] = args.image_dir
    os.environ['leaflabeler_image_list'] = args.image_list
    os.environ['leaflabeler_label_output_file'] = args.label_output_file

    from django.core.management import execute_from_command_line

    #execute_from_command_line(sys.argv)
    execute_from_command_line([sys.argv[0], 'runserver'])     # hardcode runserver command



if __name__ == "__main__":
    main()
