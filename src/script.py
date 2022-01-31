import requests
import datetime
import json

SLACK_API_URL = "https://slack.com/api/chat.postMessage"
SLACK_CHANNEL = "xxxxxx"
USER_OAUTH_TOKEN = "xoxp-xxxxxx-xxxxxx-xxxxxx-xxxxxx"

def get_event_list():
    today = datetime.date.today()
    yyyymm = today.strftime('%Y%m')
    url = "https://connpass.com/api/v1/event/?keyword=QA&ym=" + yyyymm

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()

def create_thread_at_slack():
    payload = json.dumps({
    "channel": SLACK_CHANNEL,
    "text": "今月のQAイベントまとめスレ"
    })
    headers = {
    'Authorization': 'Bearer ' + USER_OAUTH_TOKEN,
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", SLACK_API_URL, headers=headers, data=payload)
    return response.json()["ts"]

def post_event_info_to_slack(ts, event_info):
    payload = json.dumps({
    "channel": SLACK_CHANNEL,
    "thread_ts": ts,
    "text": event_info
    })
    headers = {
    'Authorization': 'Bearer ' + USER_OAUTH_TOKEN,
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", SLACK_API_URL, headers=headers, data=payload)

def lambda_handler(event, context):
    ts = create_thread_at_slack()
    response = get_event_list()
    for event in response["events"]:
        event_info = "イベントID:" + str(event["event_id"]) + "\n"\
            + "イベントタイトル:" + event["title"] + "\n"\
            + "キャッチ:" + event["catch"] + "\n"\
            + "開始日時:" + event["started_at"] + "\n"\
            + "終了日時:" + event["ended_at"] + "\n"\
            + "参加可能人数:" + str(event["limit"]) + "\n"\
            + "参加人数:" + str(event["accepted"]) + "\n"\
            + "URL:" + event["event_url"]
        post_event_info_to_slack(ts, event_info)
