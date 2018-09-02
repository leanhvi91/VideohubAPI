from local_utils import wrap_response

# bucket_name = "videohub-vn"
# path = "videohub-vn/subtitles"


# def load_subtitle(videoId):
#     key = path + "/" + videoId + ".srt"
#     s3 = boto3.client("s3")
#     result = s3.get_object(Bucket=bucket_name, Key=key)
#     raw_content = result["Body"].read().decode()
#     return wrap_response(raw_content)
#
#
# def put_subtitle(videoId, content):
#     s3 = boto3.client('s3')
#     key = path + "/" + videoId + ".srt"
#     try:
#         s3.put_object(Body=content, Bucket=bucket_name, Key=key)
#         return wrap_response("Upload success: %s" % path)
#     except Exception as e:
#         return wrap_response("Upload failed: %s" % path)


def get_millis_sec(time_str):
    """
    Get millisecond from time string. E.g: 00:02:55,000 -> 175000 (millisecond)
    :param time_str:
    :return:
    """
    time_str = time_str.strip()
    t = time_str.split(":")
    h = int(t[0].strip())
    m = int(t[1].strip())
    if "." in t[2]:
        sep = "."
    if "," in t[2]:
        sep = ","
    if sep:
        _s = t[2].split(sep)
        s = int(_s[0].strip())
        ms = int(_s[1].strip())
    else:
        s = 0
        ms = int(t[2])
    return 3600000*h + 60000*m + 1000*s + ms


def parse_json(content):
    """
    Load srt file into list of subtitle object
    :param content: srt format
    :return: parsed to json object
    """
    content = content.strip()
    lines = content.split("\n\n")
    sub = []
    for line in lines:
        try:
            num, time_line, text = line.split("\n")
            print(num)
            begin, end = time_line.split("-->")
            begin = get_millis_sec(begin)
            end = get_millis_sec(end)
            obj = {
                "num" : num,
                "begin": begin,
                "end": end,
                "text": text
            }
            sub.append(obj)
        except:
            continue
    return sub


if __name__ == "__main__":
    file_path = "/home/vila/projects/DayTooSoon/oHHBLSSctoc.srt"


    f = open(file_path, "r")
    content = f.read()
    subs = parse_json(content)

    import json
    txt = json.dumps(subs, indent=2, ensure_ascii=False)

    f = open("/home/vila/projects/DayTooSoon/oHHBLSSctoc.json", "w")
    f.write(txt)










