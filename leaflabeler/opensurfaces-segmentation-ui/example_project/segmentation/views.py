import json
import pprint
import pdb

from ua_parser import user_agent_parser

from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import Http404, HttpResponse
from django.conf import settings

from .forms import LabelerIDForm

from labeler import LeafLabeler
# Define a global leaflabeler object
if not 'leaflabeler' in locals() or 'leaflabeler' in globals():
    leaflabeler = LeafLabeler()


def check_stage_and_redirect(current_page_stage = None):
    current_stage = leaflabeler.get_stage()
    #print 'current_stage is', current_stage, 'on page', current_page_stage
    
    if current_page_stage != current_stage:
        return redirect(current_stage)


@ensure_csrf_cookie
def label(request):
    """
    Serve up a segmentation task.

    This is a demo, so we are going to hard-code an image to tag.
    In a live system, you would read the HIT id:
        hit_id = request.REQUEST['hitId']
        assignment_id = request.REQUEST['assignmentId']
    and fetch a photo from the database.

    When a user submits, the data will be in request.body.
    request.body will contain these extra fields corresponding
    to data sent by the task window:

        results: a dictionary mapping from the content.id (which is just "1" in
            this example) to a list of polygons.  Example:
            {"1": [[x1,y1,x2,y2,x3,y3,...], [x1,y1,x2,y2,...]]}.
            The x and y coordinates are fractions of the width and height
            respectively.
        time_ms: amount of time the user spent (whether or not
            they were active)
        time_active_ms: amount of time that the user was
            active in the current window
        action_log: a JSON-encoded log of user actions
        screen_width: user screen width
        screen_height: user screen height
        version: always "1.0"

        If the user gives feedback, there will also be this:
        feedback: JSON encoded dictionary of the form:
        {
            'thoughts': user's response to "What did you think of this task?",
            'understand': user's response to "What parts didn't you understand?",
            'other': user's response to "Any other feedback, improvements, or suggestions?"
        }

    """

    #print 'On this request, leaflabeler is', leaflabeler
    redir = check_stage_and_redirect('label')
    if redir: return redir
    
    # replace this with a fetch from your database
    if request.method == 'POST':
        # this will return the POST data back to the client in the form of an
        # error message (so you can inspect it).
        pp = pprint.PrettyPrinter(indent=4)

        posted_data = request.POST.dict()
        #print 'Got data:'
        #pp.pprint(posted_data)

        results = json.loads(posted_data['results'])
        #print 'keys are', results.keys()
        assert len(results.keys()) == 1, 'Expected a single image key'
        imkey = int(results.keys()[0])
        leaflabeler.update_label(posted_data)

        leaflabeler.write_to_file()
        
        #return json_error_response(
        #    "This is a demo.  Here is the data you submitted: " +
        #    json.dumps(request.POST))

        # to instead signal that the data was properly submitted, return a JSON
        # object indicating success (see below commented line).  The client
        # will then tell the MTURK server that the task was completed.
        # See segmentation/static/jss/mturk/mt_submit.coffee (search for
        # window.location) for the code that does this on the client side.

        return json_success_response()
    else:
        response = browser_check(request)
        if response:
            return response

        # hard-coded example image:
        iminfo = leaflabeler.get_next_image()
        #print 'Next image', iminfo
        if iminfo == None:
            return redirect('done')
        else:
            imkey, imname = iminfo
            
        context = {
            # the current task
            'content': {
                # the database ID of the photo.  You can leave this at 1 if you
                # don't use a database.  When the results are submitted, the
                # content.id is the key in a dictionary holding the polygons.
                'id': imkey,
                # url where the photo can be fetched.
                #'url': 'http://farm9.staticflickr.com/8204/8177262167_d749ec58d9_h.jpg'
                #'url': 'http://s.yosinski.com/example_nlb.jpg'
                'url': settings.MEDIA_URL + imname
            },

            # min number of shapes before the user can submit
            'min_shapes': 0,

            # min number of vertices the user must click for each shape
            'min_vertices': 3,

            # if 'true', ask the user a feedback survey at the end and promise
            # payment to complete it.  Must be 'true' or 'false'.
            'ask_for_feedback': 'false',

            # feedback_bonus is the payment in dollars that we promise users
            # for completing feedback
            'feedback_bonus': 0.02,

            # template containing html for instructions
            'instructions': 'mturk/mt_segment_material_inst_content.html'
        }

    rendered = render(request, 'mturk/mt_segment_material.html', context)
    #print 'returning rendered'
    return rendered

    
@ensure_csrf_cookie
def start(request):
    redir = check_stage_and_redirect('start')
    if redir: return redir
    
    if request.method == 'POST':
        form = LabelerIDForm(request.POST)

        if form.is_valid():
            leaflabeler.update_labeler_id(form.cleaned_data['labeler_id'])

            # Start labeling now
            return redirect('label')

    else:
        form = LabelerIDForm()

    return render(request, 'mturk/mt_segment_start.html', {'form': form})


@ensure_csrf_cookie
def done(request):
    redir = check_stage_and_redirect('done')
    if redir: return redir

    context = {
        'n_images': leaflabeler.n_images,
        'image_list': leaflabeler.image_list,
    }
    return render(request, 'mturk/mt_segment_done.html', context)
    

def browser_check(request):
    """ Only allow firefox and chrome, and no mobile """
    valid_browser = False
    if 'HTTP_USER_AGENT' in request.META:
        ua = user_agent_parser.Parse(request.META['HTTP_USER_AGENT'])
        if ua['user_agent']['family'].lower() in ('firefox', 'chrome'):
            device = ua['device']
            if 'is_mobile' not in device or not device['is_mobile']:
                valid_browser = True
    if not valid_browser:
        return html_error_response(
            request, '''
            This task requires Google Chrome. <br/><br/>
            <a class="btn" href="http://www.google.com/chrome/"
            target="_blank">Get Google Chrome</a>
        ''')
    return None


def json_success_response():
    return HttpResponse(
        '{"message": "success", "result": "success"}',
        content_type='application/json')


def json_error_response(error):
    """ Return an error as a JSON object """
    return HttpResponse(
        json.dumps({'result': 'error', 'message': error}),
        content_type='application/json')


def html_error_response(request, error):
    return render(request, "error.html", {'message': error})
