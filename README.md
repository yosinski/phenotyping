# Phenotyping labeler and other code



# Installing the labeler

First, grab the code

    $ git clone https://github.com/yosinski/phenotyping.git
    $ cd phenotyping
    
It's easiest to run the labeler from within a Python [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/), so the packages live completely separately from the other installed packages on your system. The prevents version conflicts, etc. First install virtualenv, and then make and activate one for this project. On my system, this process looked like the following, though your setup may vary:

Creation:

    $ mkdir -p ~/virtualenvs
    $ virtualenv ~/virtualenvs/phenotyping

Activation (must be run in each shell in which you wish to run the lableler. Consider adding to your `~/.bashrc` to run it automatically in every shell).

    $ . ~/virtualenvs/phenotyping/bin/activate
    
Next, install the Python packages necessary for the labeler inside the virtualenv using pip:

    $ pip install -r requirements.txt

That's it!

# Running the labeler

To run the labeler, first put all the images you're considering labeling in some directory. Here, I've put them in the `phenotyping/images` directory (but you could put them elsewhere).

Next, create a text file listing the images you'd like to collect labels for, listing one image filename per line. Here's an example:

    $ cat images_000.txt
    nlb1.jpg
    nlb2.jpg
    nlb3.jpg

Then, run the labeler using `run_labeler.py`:

    $ ./run_labeler.py images collected_labels/images_001.txt collected_labels/labels_001.pkl

See the script help for more information if desired:

    $ ./run_labeler.py --help
    
Basically, the three required arguments are the path to the directory containing the images, the path to the text file containing image filenames to be labeled on this run, and the path to the file you'd like to write the labels to. In this case, we'll output labels (in Python pickle format) to the file `collected_labels/labels_001.pkl`. This file does not need to exist before the program starts (actually, if it does, it will be overwritten).

So, assuming the labeler is running using the command above, the webserver will now be serving pages on 127.0.0.1:8000. Visit that page in your browser to begin the labeling process: [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

# Checking out the labels

The label file is just a Python dict stored in pickle format. It's easy to load, for example, via the `peek_labels.py` script:

    $ ./peek_labels.py collected_labels/labels_001.pkl
    File collected_labels/labels_000.pkl content summary:
      version:                    1
      image directory used:       images
      image list used:            collected_labels/images_000.txt
      number of images:           3
        first image filename:     nlb1.jpg
      number of labels collected: 3
        first label:              {u'screen_width': u'1440', u'time_ms': u'{"0":[4623,2154,2020,5889]}',
                                  u'results': u'...

To output information in other formats, you can make your own script like `peek_labels.py` that does something different, like computes bounding boxes and writes them to a separate file, or samples square regions and assigns them label -1 or +1 based on their overlap with labeled polygon regions, or ...

# Possible improvements

* Add the ability to submit the current polygon set by using the keyboard instead of clicking on the "Submit" button.
* Add other types of drawing, e.g. single straight line via two clicks
