from flask import Flask, request, make_response, Response
from mediaplaycounts.MediaPlaycounts.GetData.FilePlaycount import date as fpc_date, date_range as fpc_date_range, last_30 as fpc_last_30, last_90 as fpc_last_90
from mediaplaycounts.MediaPlaycounts.GetData.CategoryPlaycount import date as cpc_date, date_range as cpc_date_range, last_30 as cpc_last_30, last_90 as cpc_last_90
from mediaplaycounts.MediaPlaycounts.GetData.AskCommons import find_subcategories, find_media_files
import json

# I've been doing too much JavaScript
true = True
false = False

app = Flask(__name__)

def _api_response(payload):
    resp = make_response(json.dumps(payload))
    resp.headers["Content-Type"] = "application/json"
    return resp


@app.route('/')
def home():
    return Response("Wow!")

@app.route('/api')
def apihome():
    info = {"current_version": 1, "all_versions": [1]}
    return _api_response(info)

@app.route('/api/1')
def list_current_methods():
    info = {"methods": ["FilePlaycount", "CategoryPlaycount", "AskCommons"]}
    return _api_response(info)

@app.route('/api/1/FilePlaycount')
def fileplaycount_directory():
    info = {"methods": ["date", "date_range", "last_30", "last_90"]}
    return _api_response(info)

@app.route('/api/1/CategoryPlaycount')
def categoryplaycount_directory():
    info = {"methods": ["date", "date_range", "last_30", "last_90"]}
    return _api_response(info)

@app.route('/api/1/AskCommons')
def askcommons_directory():
    info = {"methods": ["find_subcategories", "find_media_files"]}
    return _api_response(info)

@app.route('/api/1/FilePlaycount/date')
def fileplaycount_date_doc():
    info = {"parameters": [
                            {"@label": "filename",
                             "@notes": "Do not include the 'File:' prefix.",
                             "type": "string",
                             "required": true},
                            {"@label": "date",
                             "@notes": "Format must be YYYYMMDD",
                             "type": "string",
                             "required": true}
                          ]
           }
    return _api_response(info)

@app.route('/api/1/FilePlaycount/date/<filename>/<date>')
def fileplaycount_date(filename, date):
    info = fpc_date(filename, date)
    return _api_response(info)

@app.route('/api/1/FilePlaycount/date_range')
def fileplaycount_date_range_doc():
    info = {"parameters": [
                            {"@label": "filename",
                             "@notes": "Do not include the 'File:' prefix.",
                             "type": "string",
                             "required": true},
                            {"@label": "start_date",
                             "@notes": "Format must be YYYYMMDD and must be chronologically earlier than end_date",
                             "type": "string",
                             "required": true},
                            {"@label": "end_date",
                             "@notes": "Format must be YYYYMMDD and must be chronologically later than start_date",
                             "type": "string",
                             "required": true}
                          ]
           }
    return _api_response(info)

@app.route('/api/1/FilePlaycount/date_range/<filename>/<start_date>/<end_date>')
def fileplaycount_date_range(filename, start_date, end_date):
    info = fpc_date_range(filename, start_date, end_date)
    return _api_response(info)

@app.route('/api/1/FilePlaycount/last_30')
def fileplaycount_last_30_doc():
    info = {"parameters": [
                            {"@label": "filename",
                             "@notes": "Do not include the 'File:' prefix.",
                             "type": "string",
                             "required": true}
                          ]
           }
    return _api_response(info)

@app.route('/api/1/FilePlaycount/last_30/<filename>')
def fileplaycount_last_30(filename):
    info = fpc_last_30(filename)
    return _api_response(info)

@app.route('/api/1/FilePlaycount/last_90')
def fileplaycount_last_90_doc():
    info = {"parameters": [
                            {"@label": "filename",
                             "@notes": "Do not include the 'File:' prefix.",
                             "type": "string",
                             "required": true}
                          ]
           }
    return _api_response(info)

@app.route('/api/1/FilePlaycount/last_90/<filename>')
def fileplaycount_last_90(filename):
    info = fpc_last_90(filename)
    return _api_response(info)

@app.route('/api/1/CategoryPlaycount/date')
def categoryplaycount_date_doc():
    info = {"parameters": [
                            {"@label": "category",
                             "@notes": "Do not include the 'Category:' prefix.",
                             "type": "string",
                             "required": true},
                            {"@label": "date",
                             "@notes": "Format must be YYYYMMDD",
                             "type": "string",
                             "required": true},
                            {"@label": "depth",
                             "@notes": "Level of subcategory traversal",
                             "type": "number",
                             "required": false,
                             "default": 9}
                          ]
           }
    return _api_response(info)

@app.route('/api/1/CategoryPlaycount/date/<category>/<date>')
def categoryplaycount_date_autodepth(category, date):
    info = cpc_date(category, date)
    return _api_response(info)

@app.route('/api/1/CategoryPlaycount/date/<category>/<date>/<depth>')
def categoryplaycount_date_userdepth(category, date, depth):
    info = cpc_date(category, date, depth=int(depth))
    return _api_response(info)

@app.route('/api/1/CategoryPlaycount/date_range')
def categoryplaycount_date_range_doc():
    info = {"parameters": [
                            {"@label": "category",
                             "@notes": "Do not include the 'Category:' prefix.",
                             "type": "string",
                             "required": true},
                            {"@label": "start_date",
                             "@notes": "Format must be YYYYMMDD and must be chronologically earlier than end_date",
                             "type": "string",
                             "required": true},
                            {"@label": "end_date",
                             "@notes": "Format must be YYYYMMDD and must be chronologically later than start_date",
                             "type": "string",
                             "required": true},
                            {"@label": "depth",
                             "@notes": "Level of subcategory traversal",
                             "type": "number",
                             "required": false,
                             "default": 9}
                          ]
           }
    return _api_response(info)

@app.route('/api/1/CategoryPlaycount/date_range/<category>/<start_date>/<end_date>')
def categoryplaycount_date_range_autodepth(category, start_date, end_date):
    info = cpc_date_range(category, start_date, end_date)
    return _api_response(info)

@app.route('/api/1/CategoryPlaycount/date_range/<category>/<start_date>/<end_date>/<depth>')
def categoryplaycount_date_range_userdepth(category, start_date, end_date, depth):
    info = cpc_date_range(category, start_date, end_date, depth=int(depth))
    return _api_response(info)

@app.route('/api/1/CategoryPlaycount/last_30')
def categoryplaycount_last_30_doc():
    info = {"parameters": [
                            {"@label": "category",
                             "@notes": "Do not include the 'Category:' prefix.",
                             "type": "string",
                             "required": true},
                            {"@label": "depth",
                             "@notes": "Level of subcategory traversal",
                             "type": "number",
                             "required": false,
                             "default": 9}
                          ]
           }
    return _api_response(info)

@app.route('/api/1/CategoryPlaycount/last_30/<category>')
def categoryplaycount_last_30_autodepth(category):
    info = cpc_last_30(category)
    return _api_response(info)

@app.route('/api/1/CategoryPlaycount/last_30/<category>/<depth>')
def categoryplaycount_last_30_userdepth(category, depth):
    info = cpc_last_30(category, depth=int(depth))
    return _api_response(info)

@app.route('/api/1/CategoryPlaycount/last_90')
def categoryplaycount_last_90_doc():
    info = {"parameters": [
                            {"@label": "category",
                             "@notes": "Do not include the 'Category:' prefix.",
                             "type": "string",
                             "required": true},
                            {"@label": "depth",
                             "@notes": "Level of subcategory traversal",
                             "type": "number",
                             "required": false,
                             "default": 9}
                          ]
           }
    return _api_response(info)

@app.route('/api/1/CategoryPlaycount/last_90/<category>')
def categoryplaycount_last_90_autodepth(category):
    info = cpc_last_90(category)
    return _api_response(info)

@app.route('/api/1/CategoryPlaycount/last_90/<category>/<depth>')
def categoryplaycount_last_90_userdepth(category, depth):
    info = cpc_last_90(category, depth=int(depth))
    return _api_response(info)

@app.route('/api/1/AskCommons/find_subcategories')
def askcommons_find_subcategories_doc():
    info = {"parameters": [
                            {"@label": "category",
                             "@notes": "Do not include the 'Category:' prefix.",
                             "type": "string",
                             "required": true},
                            {"@label": "depth",
                             "@notes": "Level of subcategory traversal",
                             "type": "number",
                             "required": false,
                             "default": 9}
                          ]
           }
    return _api_response(info)

@app.route('/api/1/AskCommons/find_subcategories/<category>')
def askcommons_find_subcategories_autodepth(category):
    info = find_subcategories(category)
    return _api_response(info)

@app.route('/api/1/AskCommons/find_subcategories/<category>/<depth>')
def askcommons_find_subcategories_userdepth(category, depth):
    info = find_subcategories(category, depth=int(depth))
    return _api_response(info)

@app.route('/api/1/AskCommons/find_media_files')
def askcommons_find_media_files_doc():
    info = {"parameters": [
                            {"@label": "category",
                             "@notes": "Do not include the 'Category:' prefix.",
                             "type": "string",
                             "required": true}
                          ]
           }
    return _api_response(info)

@app.route('/api/1/AskCommons/find_media_files/<category>')
def askcommons_find_media_files(category):
    info = find_media_files(category)
    return _api_response(info)

