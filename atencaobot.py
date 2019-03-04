import tweepy
import time
import random
import asyncio
from threading import Thread
import json

def cnt_word(s, w):
    return f' {w} ' in f' {s} '

async def verifyIDs(id):
    file = open("tweetIDS.txt").readlines();
    idList = file[0].split(",");

    if idList.__contains__(str(id)):
        return True;
    else:
        return False;

def followingPeople(i):
    print("Following thread started!");
    while True:
        time.sleep(60*10);
        for follower in tweepy.Cursor(api.followers).items():
            follower.follow();
        print("Followed everyone back!")

# https://stackoverflow.com/questions/37098552/tweepy-api-limit-workaround
def twitter_rates():
    stats = api.rate_limit_status()  #stats['resources'].keys()
    for akey in stats['resources'].keys():
        if type(stats['resources'][akey]) == dict:
            for anotherkey in stats['resources'][akey].keys():
                if type(stats['resources'][akey][anotherkey]) == dict:
                    #print(akey, anotherkey, stats['resources'][akey][anotherkey])
                    limit = (stats['resources'][akey][anotherkey]['limit'])
                    remaining = (stats['resources'][akey][anotherkey]['remaining'])
                    used = limit - remaining

                    if anotherkey == "/search/tweets":
                        if remaining == 1:
                            api.update_status("vou descansar por um tempinho, depois volto...");
                    if used != 0:
                        print("Twitter API used", used, "remaining queries", remaining,"for query type", anotherkey)
                    else:
                        pass
                else:
                    pass  #print("Passing")  #stats['resources'][akey]
        else:
            print(akey, stats['resources'][akey])
            print(stats['resources'][akey].keys())
            limit = (stats['resources'][akey]['limit'])
            remaining = (stats['resources'][akey]['remaining'])
            used = limit - remaining
            if used != 0:
                print("Twitter API:", used, "requests used,", remaining, "remaining, for API queries to", akey)
                pass

with open('config.json') as f:
    data = json.load(f)

consumer_key = data["consumer_key"];
consumer_secret = data["consumer_secret"];
access_token = data["access_token"];
access_token_secret = data["access_token_secret"];
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

user = api.me()
print("bot name:" + user.name);

frases = ["TOMA ATENÇAO AI FDP MARAVILHOS", "QUER ATENÇAO??? TOMA ENTAO DESGRAÇA LINDA",
          "NAMORAL??? TOMA ATENCAO AI PQ VC MERECE", "ATENÇAO???? TOMA <<<<", "OI COISA LINDA TD BEM???? TOMA ATENÇAO KRL",
          "YOU JUST WANT ATTENTION\nYOU DONT WANT MY HEART\nENTAO TOMA ATTENTION"];

lastTweet = "";

t = Thread(target=followingPeople, args=(1,));
t.start();

while True:
    twitter_rates();

    f = open("tweetIDS.txt", "a+")

    print("\n========\nsleeping...\n=======\n");

    time.sleep(5);

    print("Searching...");
    results = api.search(q="@atencao_bot", count=5);
    print("SEARCH SUCESSFUL!");

    if (asyncio.run(verifyIDs(results[0].id))):
        print("Already replied to that tweet!");
        print(results[0].id);
        print("=======");
        print("\n");
    else:
        print("@" + results[0].user.screen_name + " - " + results[0].text + "\n\n");

        api.update_status("@" + results[0].user.screen_name + " " + frases[random.randint(0, len(frases) - 1)] + " (x" + str(random.randint(0,100000)) + ")", in_reply_to_status_id=results[0].id);
        f.write(str(results[0].id)+",");
        f.close();
        print("=======");
        print("\n");
