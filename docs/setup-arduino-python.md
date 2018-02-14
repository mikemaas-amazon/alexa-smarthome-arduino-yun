### Copy the Python code to the Arduino

If you are developing with MacOS, you can use SCP directly. If using Windows, you can use WinSCP.

Connect to the Arduino YÚN device as _root_ and copy over the files generated during the AWS IoT thing creation into the /root directory:

- aws-iot-rootCA.crt file.
- {XXXXXXXXXX}.cert.pem
- {XXXXXXXXXX}.private.key

> The cert.pem and private.key files will be unique for the device created.

#### Edit and copy the MQTT client script

In the source /arduino directory, edit the client-light.py file and update the ```!!! Configuration settings !!!``` section. 

- thing_name = 'arduino-sample'
- thing_endpoint = 'a311mxzpj0i4v.iot.us-east-1.amazonaws.com'
- thing_aws_root_cert = 'aws-iot-rootCA.crt'  # Something like aws-iot-rootCA.crt
- thing_private_key = 'arduino-test.private.key'  # Something like arduino-test.private.key
- thing_cert = 'arduino-test.cert.pem'  # Something like arduino-test.cert.pem


From the source /arduino directory, copy the client-light.py file.


Once edited and saved, copy the client-light.py Python script to the Arduino YÚN.


While connected via SSH, you can run the command to start the MQTT client in the background:

```
python client-light.py &
```


[Continue with the Setup](setup.md)