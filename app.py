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
        indexcount = -1#検索インデックスを初期化(1回目は0にする為-1で初期化)
        for value1 in infodict.values():#アカウント別リストを纏める
            indexcount+=1#インデックスを加算
            for value2 in value1:#リストのリストをforで回す
                if status.user.screen_name in value2:#ツイートユーザーが登録リストに入っている場合
                    api.send_direct_message(screen_name=list(infodict.keys())[int(indexcount):int(indexcount+1)][0], text="あなたのフォロワーの #コンパス履歴書 が更新されました！\ntwitter.com/"+str(status.user.screen_name)+"/status/"+str(status.id))
                    #インデックスよりアカウントのリスト番号から抜き出してDM送信
    def on_error(self, status):
        print(status)
class DMListener(tweepy.streaming.StreamListener):
    def on_data(self, status):
        if 'direct_message' in status:#DM処理
            dm = json.loads(status)['direct_message']
            # print('DM: {} from @{}'.format(dm['text'], dm['sender_screen_name']))
            if dm['text'] == '登録':
                FollowersList=getFollowers_ids(api, Id = dm['sender_screen_name'])
                if len(FollowersList) == 0:#フォロワーリストの確認(鍵垢の場合0になる。)
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
        followers_ids = tweepy.Cursor(api.followers_ids, id = Id, cursor = -1).items()#フォロワーを内部IDで取得
    except:
        return []#失敗した場合空のリストで返す(処理上問題なし)
    else:
        ids = []#str変換のバッファ用リストを初期化
        for f in followers_ids:#idリストをintからstrに変換
            ids.append(str(f))
        idcount = len(ids)#全id数を確認
        finalscreenname=[]#最終出力を初期化
        while idcount != 0:#残り未処理idが0になるまで繰り返す
            idlist=[]#処理idリストを初期化
            idlist = ids[:100]#最初から100までのidを取得し処理idリストに代入
            ids[:100]=[]#代入が完了したidを削除
            idcount = len(ids)#残り未処理id数を更新
            for name in api.lookup_users(user_ids=idlist):#リストからアカウントをルックアップして名前を取得
                finalscreenname.append(name.screen_name)
        return finalscreenname#名前のリストを返す
if __name__ == '__main__':
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit = True)
    TimeLine = TimeLineListener()
    stream = tweepy.Stream(auth, TimeLine)
    stream.filter(track = ["#コンパス履歴書"],async=True)#コンパス履歴書のタグに限りストリームをフィルタ
    DM=DMListener()
    stream2 = tweepy.Stream(auth, DM)
    stream2.userstream(async=True)
