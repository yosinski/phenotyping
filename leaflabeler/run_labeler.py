#! /usr/bin/env python2.7

import os
import sys
import argparse



def main():
    parser = argparse.ArgumentParser(description='Main script for running LeafLabeler')
    parser.add_argument('infile', type = str, help = 'Which file to load')
    parser.add_argument('outfile', type = str, help = 'Which file to output')
    args = parser.parse_args()

    proj_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'opensurfaces-segmentation-ui', 'example_project')
    print 'inserting', proj_dir
    sys.path.insert(0, proj_dir)
                    
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "example_project.settings")
    os.environ['leaflabeler_infile'] = 'foo_in'
    os.environ['leaflabeler_outfile'] = 'foo_out'

    from django.core.management import execute_from_command_line

    #execute_from_command_line(sys.argv)
    execute_from_command_line(['./foo.py', 'runserver'])



if __name__ == "__main__":
    main()
