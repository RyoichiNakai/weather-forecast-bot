import requests
from bs4 import BeautifulSoup


class GetCoordinate:

    # geocoding.jpのapi
    url = 'http://www.geocoding.jp/api/'

    def __init__(self, address):

        address_query = {'q': address}
        self.html = requests.get(self.url, params=address_query)

    def coordinate(self):

        """
        addressに住所を指定すると緯度経度を返す。

        coordinate('東京都文京区本郷7-3-1')
        ['35.712056', '139.762775']
        """

        soup = BeautifulSoup(self.html.text, 'html.parser')

        if soup.find('error'):
            raise ValueError(f"Invalid address submitted.")

        # 緯度と経度を返す
        latitude = soup.find('lat').string
        longitude = soup.find('lng').string

        return [latitude, longitude]


if __name__ == "__main__":
    input_text = '函館'
    r = GetCoordinate(input_text)
    reply = r.coordinate()
    print(reply)
