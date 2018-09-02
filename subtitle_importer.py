import requests
import xml.etree.ElementTree as ET
import html
from local_utils import wrap_response


def load_subtitle(videoId, lang):
    """

    :param videoId:
    :param lang:
    :return:
    """
    api_url = "https://www.youtube.com/api/timedtext"
    querystring = {
        "v": videoId,
        "lang": lang
    }
    headers = {
        'cache-control': "no-cache",
        'postman-token': "43b73caf-e525-0535-56cc-4490c4a7ac1c"
    }
    response = requests.request("GET", api_url, headers=headers, params=querystring)
    if not response.ok:
        print("%s\tSUBTITLE NOT FOUND" % videoId)
        return []
    if not response.text.strip():
        querystring["lang"] = "en"
        querystring["tlang"] = lang
        response = requests.request("GET", api_url, headers=headers, params=querystring)
    if not response.ok or not response.text.strip():
        print("%s\tSUBTITLE NOT FOUND" % videoId)
        return []
    lines = []
    root = ET.fromstring(response.text)
    for child in root:
        time = child.attrib
        text = child.text
        line = {}
        if "start" in time and "dur" in time:
            line["start"] = time["start"]
            line["dur"] = time["dur"]
            line["text"] = html.unescape(text)
            lines.append(line)
    print("%s\tSUCCESS DOWNLOAD" % videoId)
    return lines


def lambda_handler(event, context):

    try:
        video_id = event["queryStringParameters"]["videoId"]
        lang = event["queryStringParameters"]["lang"]
    except Exception as e:
        return wrap_response("You must provide videoId and lang \n Stack trace %s" % e)

    lines = load_subtitle(videoId=video_id, lang=lang)
    return wrap_response(lines)