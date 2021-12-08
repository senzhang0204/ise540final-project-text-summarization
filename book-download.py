import http
import urllib.request
from tqdm import tqdm


for s in ['history', 'fiction', 'biography', 'fable', 'story', 'tale', 'journal']:
    with open(f'book_{s}.csv', 'r') as f:
        urls = set([i[:-1] for i in f.readlines()])
        print(len(urls))
for s in ['history', 'fiction', 'biography', 'fable', 'story', 'tale', 'journal']:
    with open(f'book_{s}.csv', 'r') as f:
        urls = set([i[:-1] for i in f.readlines()])
        for url in tqdm(urls):
            # print(url)
            try:
                response = urllib.request.urlopen(url)
                data = response.read()  # a `bytes` object
                text = data.decode('utf-8')  # a `str`
                with open(f'{s}/' + url.split('/')[-1][:-6], 'w+') as o:
                    o.write(text)
            # except urllib.error.HTTPError:
            #     print('skip url')
            #     pass
            except UnicodeDecodeError:
                print('decoding error')
                pass
            except:
                pass
