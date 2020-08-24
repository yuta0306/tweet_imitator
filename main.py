from twitter import Twitter
from trigram import Trigram
from corpus import create_corpus, reconstruct_corpus

if __name__ == "__main__":
    """Main program"""
    
    tw = Twitter()
    corpus = tw.fecth_tweets(3000, wait=True)
    create_corpus(corpus, 'tweets')

    corpus = reconstruct_corpus('tweets.pickle')

    trigram = Trigram(corpus=corpus)

    print('以下の単語群から文章を開始することができます')
    for usage in sorted(list(trigram.usage_)):
        print(usage, end=' / ')
    
    try:
        while True:
            word = input('\n開始単語を1語入力してください:')
            sentence = trigram.generate(word)
            print(sentence)
            print('============================')
            tweet = input('ツイートしますか? (Y/n)')
            if tweet == 'Y':
                tw.update_tweet(sentence)
        
            input('プログラム終了次は`Ctrl+C`を押してください\n\
            続ける場合はそのほかのキーを押してください')

    except KeyboardInterrupt:
            print('\n\n~~~プログラム終了~~~')
