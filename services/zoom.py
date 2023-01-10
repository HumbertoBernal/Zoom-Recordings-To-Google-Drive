import http.client
import datetime
import json
import jwt


def generate_jwt(API_KEY, API_SECRET):
    payload = {'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30),
               'iss': API_KEY
               }
    return jwt.encode(payload, API_SECRET)


def get_meeting_recordings(token, meeting_id):
    
    conn = http.client.HTTPSConnection("api.zoom.us")
    headers = {'authorization': "Bearer " + token}
    
    conn.request(
        "GET", f"/v2/meetings/{meeting_id}/recordings", headers=headers)

    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))
    return data

def set_recording_settings(token, meeting_id):
    
    conn = http.client.HTTPSConnection("api.zoom.us")
    headers = {'authorization': "Bearer " + token}

    body = {
        "viewer_download": True
    }
    
    conn.request(
        "PATCH", f"/v2/meetings/{meeting_id}/recordings/setttings", json.dumps(body), headers=headers)

    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))
    return data


def delete_recording(meeting_id, token):
    """ 
    Delete Zoom event
    """
    conn = http.client.HTTPSConnection("api.zoom.us")
    headers = { 'authorization': "Bearer " + token, }

    conn.request(
        "DELETE", f"/v2/meetings/{meeting_id}/recordings", headers=headers)

    res = conn.getresponse()
    data = res.read()

    return data.decode("utf-8")
