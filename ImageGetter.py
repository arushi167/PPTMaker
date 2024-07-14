import requests
import random
import string
import threading

class ImageGetter:
    def __init__(self, access_key):
        self.access_key = access_key
        self.base_url = "https://api.unsplash.com/photos/random"
        self.params = {
            "orientation": "landscape",
            "query": "",
            "w": 256,
            "h": 144,
            "client_id": self.access_key
        }

    def _download_image(self, url, filename):
        r = requests.get(url, allow_redirects=True)
        final_url = r.json()["url"]
        r = requests.get(final_url, allow_redirects=True)
        open(filename, 'wb').write(r.content)

    def get_image_paths(self, topic, json_data):
        threads = []
        slide_image_paths = {}  # Dictionary to store image paths based on slide number

        def download_image_thread(slide):
            heading = slide.get("heading", "default")
            slide_number = slide.get("slide", 1)
            letters = string.ascii_lowercase
            filename = f'{"".join(random.choice(letters) for _ in range(6))}.jpg'
            image_url, html_credit = self.get_image_url(topic+" Heading: "+heading)
            if image_url:
                image_path = "static/images/ppt_img/" + filename
                self._download_image(image_url, image_path)
                slide_image_paths[slide_number] = {
                    "image_path": image_path,
                    "html_credit": html_credit
                }

        for slide in json_data.get("content", []):
            thread = threading.Thread(target=download_image_thread, args=(slide,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        sorted_image_paths = [slide_image_paths[key] for key in sorted(slide_image_paths.keys())]
        # [{"image_path": "", "html_credit": ""}, {"image_path": "", "html_credit": ""}]
        return sorted_image_paths

    def get_image_url(self, topic):
        self.params["query"] = topic
        response = requests.get(self.base_url, params=self.params)
        if response.status_code == 200:
            img_response = response.json()
            # import pprint 
            # pprint.pprint(img_response)
            img_url = img_response["links"]["download_location"] + "&client_id=" + self.access_key


            credit_url = img_response["user"]["links"]["html"]
            username   = img_response["user"]["name"]
            img_unsplash_link = img_response["links"]["html"]
            html_credit = f'Photo by <a href="{credit_url}?utm_source=makeit.witeso.com&utm_medium=referral">{username}</a> on <a href="{img_unsplash_link}?utm_source=makeit.witeso.com&utm_medium=referral">Unsplash</a>'
            return img_url, html_credit
        else:
            return None  
    
if __name__ == "__main__":
    test = ImageGetter("btnHAFhjy2uuVUWDUYGOMd_lHwJr3AVQNV4AyPPNqLc")
    image_url, html_credit = test.get_image_url("Bugati")
    print("[+] Img URL: ", image_url)
    print("[+] HTML Credit: ", html_credit)
    if image_url:
        image_path = "static/images/ppt_img/" + "bugati.jpg"
        test._download_image(image_url, image_path)
