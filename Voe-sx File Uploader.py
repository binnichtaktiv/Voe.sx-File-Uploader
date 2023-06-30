import json, requests, os
from tqdm import tqdm
from requests_toolbelt.multipart.encoder import MultipartEncoder, MultipartEncoderMonitor

API_KEY = "abc"  
FILE_PATH = input("Enter .mp4 file path:\n")  

url_step1 = f"https://voe.sx/api/upload/server?key={API_KEY}"
response_step1 = requests.get(url_step1)
response_step1_data = response_step1.json()

if response_step1_data["success"]:
    upload_server_url = response_step1_data["result"]

    file_size = os.stat(FILE_PATH).st_size

    def create_callback(encoder):
        t = tqdm(total=file_size, unit='B', unit_scale=True, unit_divisor=1024)

        def callback(monitor):
            t.update(monitor.bytes_read - t.n)
        return callback

    with open(FILE_PATH, "rb") as file:
        encoder = MultipartEncoder(
            fields={"key": API_KEY, "file": (os.path.basename(FILE_PATH), file)}
        )
        monitor = MultipartEncoderMonitor(encoder, create_callback(encoder))
        headers = {"Content-Type": monitor.content_type}
        response_step2 = requests.post(upload_server_url, data=monitor, headers=headers)

    response_step2_data = response_step2.json()

    if response_step2_data["success"]:
        file_code = response_step2_data["file"]["file_code"]
        print(f"File uploaded successfully. File code: {file_code}")
    else:
        print("Error uploading the file:", response_step2_data["message"])
else:
    print("Error getting the upload server:", response_step1_data["message"])