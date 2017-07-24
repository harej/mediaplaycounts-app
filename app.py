from flask import Flask, request, make_response, Response
import mediaplaycounts.MediaPlaycounts.GetData as mpc
import json

app = Flask(__name__)


def _api_response(payload):
    resp = make_response(json.dumps(payload, indent=4))
    resp.headers["Content-Type"] = "application/json"
    return resp


def _doc_response(payload):
    resp = {'parameters': []}

    mapping = {
        'filename': {
            "@label": "filename",
            "@notes": "Do not include the 'File:' prefix.",
            "type": "string",
            "required": True
        },
        'date': {
            "@label": "date",
            "@notes": "Format must be YYYYMMDD",
            "type": "string",
            "required": True
        },
        'start_date': {
            "@label":
            "start_date",
            "@notes":
            "Format must be YYYYMMDD and must be chronologically earlier than end_date",
            "type":
            "string",
            "required":
            True
        },
        'end_date': {
            "@label":
            "end_date",
            "@notes":
            "Format must be YYYYMMDD and must be chronologically later than start_date",
            "type":
            "string",
            "required":
            True
        },
        'category': {
            "@label": "category",
            "@notes": "Do not include the 'Category:' prefix.",
            "type": "string",
            "required": True
        },
        'depth': {
            "@label": "depth",
            "@notes": "Level of subcategory traversal",
            "type": "number",
            "required": False,
            "default": 9
        }
    }

    for thing in payload:
        resp['parameters'].append(mapping[thing])

    return _api_response(resp)


### Informational ###


@app.route('/')
def home():
    return Response("Wow!")


@app.route('/api')
def apihome():
    return _api_response({"current_version": 2, "all_versions": [2]})


@app.route('/api/2')
def list_current_methods():
    return _api_response({"methods": ['file_playcount', 'category_playcount']})


@app.route('/api/2/file_playcount')
def file_playcount_directory():
    return _api_response({
        "methods": ["date", "date_range", "last_30", "last_90"]
    })


@app.route('/api/2/category_playcount')
def category_playcount_directory():
    return _api_response({
        "methods": ["date", "date_range", "last_30", "last_90"]
    })


@app.route('/api/2/file_playcount/all')
def file_playcount_date_doc():
    return _doc_response(['filename'])


@app.route('/api/2/file_playcount/date')
def file_playcount_date_doc():
    return _doc_response(['filename', 'date'])


@app.route('/api/2/file_playcount/date_range')
def file_playcount_date_range_doc():
    return _doc_response(['filename', 'start_date', 'end_date'])


@app.route('/api/2/file_playcount/last_30')
def file_playcount_last_30_doc():
    return _doc_response(['filename'])


@app.route('/api/2/file_playcount/last_90')
def file_playcount_last_90_doc():
    return _doc_response(['filename'])


@app.route('/api/2/category_playcount/all')
def category_playcount_date_doc():
    return _doc_response(['category', 'depth'])


@app.route('/api/2/category_playcount/date')
def category_playcount_date_doc():
    return _doc_response(['category', 'date', 'depth'])


@app.route('/api/2/category_playcount/date_range')
def category_playcount_date_range_doc():
    return _doc_response(['category', 'start_date', 'end_date', 'depth'])


@app.route('/api/2/category_playcount/last_30')
def category_playcount_last_30_doc():
    return _doc_response(['category', 'depth'])


@app.route('/api/2/category_playcount/last_90')
def category_playcount_last_90_doc():
    return _doc_response(['category', 'depth'])


### File Playcount ###

@app.route('/api/2/file_playcount/date/<filename>/<date>')
def file_playcount_all(filename):
    return _api_response(mpc.file_playcount(filename))


@app.route('/api/2/file_playcount/date/<filename>/<date>')
def file_playcount_date(filename, date):
    return _api_response(mpc.file_playcount(filename, end_date=date))


@app.route(
    '/api/2/file_playcount/date_range/<filename>/<start_date>/<end_date>')
def file_playcount_date_range(filename, start_date, end_date):
    return _api_response(
        mpc.file_playcount(filename, start_date=start_date, end_date=end_date))


@app.route('/api/2/file_playcount/last_30/<filename>')
def file_playcount_last_30(filename):
    return _api_response(mpc.file_playcount(filename, last=30))


@app.route('/api/2/file_playcount/last_90/<filename>')
def file_playcount_last_90(filename):
    return _api_response(mpc.file_playcount(filename, last=90))


### Category Playcount ###

@app.route('/api/2/category_playcount/all/<category>')
def category_playcount_all_autodepth(category):
    return _api_response(mpc.category_playcount(category))


@app.route('/api/2/category_playcount/all/<category>/<depth>')
def category_playcount_all_userdepth(category, depth):
    return _api_response(
        mpc.category_playcount(category, depth=int(depth)))


@app.route('/api/2/category_playcount/date/<category>/<date>')
def category_playcount_date_autodepth(category, date):
    return _api_response(mpc.category_playcount(category, end_date=date))


@app.route('/api/2/category_playcount/date/<category>/<date>/<depth>')
def category_playcount_date_userdepth(category, date, depth):
    return _api_response(
        mpc.category_playcount(category, depth=int(depth), end_date=date))


@app.route(
    '/api/2/category_playcount/date_range/<category>/<start_date>/<end_date>')
def category_playcount_date_range_autodepth(category, start_date, end_date):
    return _api_response(
        mpc.category_playcount(
            category, start_date=start_date, end_date=end_date))


@app.route(
    '/api/2/category_playcount/date_range/<category>/<start_date>/<end_date>/<depth>'
)
def category_playcount_date_range_userdepth(category, start_date, end_date,
                                            depth):
    return _api_response(
        mpc.category_playcount(
            category,
            depth=int(depth),
            start_date=start_date,
            end_date=end_date))


@app.route('/api/2/category_playcount/last_30/<category>')
def category_playcount_last_30_autodepth(category):
    return _api_response(mpc.category_playcount(category, last=30))


@app.route('/api/2/category_playcount/last_30/<category>/<depth>')
def category_playcount_last_30_userdepth(category, depth):
    return _api_response(
        mpc.category_playcount(category, depth=int(depth), last=30))


@app.route('/api/2/category_playcount/last_90/<category>')
def category_playcount_last_90_autodepth(category):
    return _api_response(mpc.category_playcount(category, last=90))


@app.route('/api/2/category_playcount/last_90/<category>/<depth>')
def category_playcount_last_90_userdepth(category, depth):
    return _api_response(
        mpc.category_playcount(category, depth=int(depth), last=90))
