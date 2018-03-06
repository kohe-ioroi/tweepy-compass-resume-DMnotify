import tweepy
# from tweepy.streaming import StreamListener
# from tweepy import OAuthHandler
# from tweepy import Stream
import json
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""
infodict={}
with open("db.json","r") as f:
    infodict=json.load(f)
class TimeLineListener(tweepy.streaming.StreamListener):
    def on_status(self, status):
        # print(status.user.name)
        # print("@"+status.user.screen_name)
        # print(status.text)
        indexcount = -1
        for value1 in infodict.values():
            indexcount+=1
            for value2 in value1:
                if status.user.screen_name in value2:
                    api.send_direct_message(screen_name=list(infodict.keys())[int(indexcount):int(indexcount+1)][0], text="あなたのフォロワーの #コンパス履歴書 が更新されました！\ntwitter.com/"+str(status.user.screen_name)+"/status/"+str(status.id))
    def on_error(self, status):
        print(status)
class DMListener(tweepy.streaming.StreamListener):
    def on_data(self, status):
        if 'direct_message' in status:
            dm = json.loads(status)['direct_message']
            # print('DM: {} from @{}'.format(dm['text'], dm['sender_screen_name']))
            if dm['text'] == '登録':
                FollowersList=getFollowers_ids(api, Id = dm['sender_screen_name'])
                if len(FollowersList) == 0:
                    api.send_direct_message(screen_name=dm['sender_screen_name'], text='フォロワーが確認できませんでした。鍵垢の場合利用できない事があります。問い合わせ先: @Kohe_Ioroi')
                else:
                    infodict[dm['sender_screen_name']]=getFollowers_ids(api, Id = dm['sender_screen_name'])
                    with open("db.json","w+") as f:
                        json.dump(infodict,f)
                    api.send_direct_message(screen_name=dm['sender_screen_name'], text='登録が完了しました。利用を停止する際は解除と送信してください。フォロワーの更新は登録と送ると行えます。')
            if dm['text'] == '解除':
                try:
                    del infodict[dm['sender_screen_name']]
                except:
                    api.send_direct_message(screen_name=dm['sender_screen_name'], text='解除に失敗しました。問い合わせ先: @Kohe_Ioroi')
                with open("db.json","w+") as f:
                    json.dump(infodict,f)
                api.send_direct_message(screen_name=dm['sender_screen_name'], text='登録を解除しました。ご利用ありがとうございました。')
    def on_error(self, status):
        print(status)
def getFollowers_ids(api, Id):
    try:
        followers_ids = tweepy.Cursor(api.followers_ids, id = Id, cursor = -1).items()
    except:
        return []
    else:
        followers_ids_list = []
        try:
            for followers_id in followers_ids:
                followers_ids_list.append(followers_id)
        except tweepy.error.TweepError as e:
            print (e.reason)
        ids = []
        for f in followers_ids_list:
            ids.append(str(f))
        idcount = len(ids)
        finalscreenname=[]
        while idcount != 0:
            idlist=[]
            idlist = ids[:100]
            ids[:100]=[]
            idcount = len(ids)
            for name in api.lookup_users(user_ids=idlist):
                finalscreenname.append(name.screen_name)
        return finalscreenname
if __name__ == '__main__':
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit = True)
    TimeLine = TimeLineListener()
    stream = tweepy.Stream(auth, TimeLine)
    stream.filter(track = ["#コンパス履歴書"],async=True)
    DM=DMListener()
    stream2 = tweepy.Stream(auth, DM)
    stream2.userstream(async=True)
