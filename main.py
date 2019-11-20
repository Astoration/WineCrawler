from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup
import os

try_cnt = 7
try_directory = str(try_cnt)+'_try'
os.mkdir(str(try_directory))
try_directory = try_directory + '/'
url = 'https://www.seoulwine.net/sub/shop/product.php?menu=shop&smenu=STC070820&mtype=product&page='
detail_url = 'https://www.seoulwine.net/sub/shop/product.php?menu=shop&smenu=&mtype=product&page=1&seq='
labels = []
index = 0
label_index = 0
list_file = open('labels.lst','w')
label_data = open('label_data','w')
for i in range(1,200):
    try:
        html = urlopen(url + str(i))
        bsObject = BeautifulSoup(html,'html.parser')
        wineTags = bsObject.select('.product-thumb-info-content .proddetail')
        for wineTag in wineTags:
            data_seq = wineTag.get('data-seq')
            wine_name = wineTag.select('h5')[0].text
            wine_name = wine_name.replace('[품절]','')
            wine_name = wine_name.replace('품절','')
            wine_name = wine_name.replace('/','\/')
            wine_name = wine_name.strip()
            try:
                has_label = labels.index(wine_name)
                if 0 <= has_label:
                    continue
            except Exception:
                print(wine_name)
            labels.append(wine_name)
            label_data.write(wine_name+'\n')
            print(data_seq)
            print(wine_name)
            continue
            has_exist = os.path.isdir(try_directory+wine_name)
            detail_html = urlopen(detail_url + str(data_seq))
            detail_bs = BeautifulSoup(detail_html,'html.parser')
            tags = detail_bs.select('.imgdiv img')
            product_images = list(map(lambda i: i.get('src'), tags))
            if False is has_exist:
                os.mkdir(try_directory+str(label_index))
            number = 1
            for image in product_images:
                print(image) 
                urlretrieve(image,try_directory+str(label_index)+'/'+str(number)+'.jpg')
                list_file.write(str(index)+'\t'+str(label_index)+'\t'+str(label_index)+'/'+str(number)+'.jpg'+'\n')
                number = number + 1
                index = index + 1
            label_index = label_index + 1
    except Exception as e:
        print(e)
list_file.close()
label_data.close()
