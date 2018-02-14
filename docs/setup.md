The setup for this sample will take about 60 minutes to complete and involves the following steps:

0. Create the required accounts
 
    **Amazon Developer Account**
    
    Go to [https://developer.amazon.com](https://developer.amazon.com) and establish an account if you do not already have one.

    **Amazon Web Services Account**

    Go to [https://aws.amazon.com](https://aws.amazon.com) and register for an Amazon Web Services (AWS) account if you do not already have one.

1. Install the required development tools and applications

    - The Arduino IDE
        - [Download the Arduino Software IDE for your platform](https://www.arduino.cc/en/Main/Software)

        The Arduino IDE is used to compile, deploy, and monitor the code running on the Arduino. The current desktop version at the time of this sample is Arduino 1.8.5.

    - A SSH client
        - On MacOS, a terminal with ```ssh```
        - On Windows, [Putty](https://putty.org/)
        
        The SSH client is used to connect to the Arduino and execute commands.
        
    - A SCP client
        - On MacOS, a terminal with ```scp```
        - On Windows, [WinSCP](https://winscp.net/eng/index.php)
    
        The SCP client is used to copy files to the Arduino.
    
    - A text editor
    
        The text editor is used to edit the sample code.
    
    Optionally you can use a Python IDE to edit the sample code:
    
    - [PyCharm Community/Professional](https://www.jetbrains.com/pycharm/)
    - [Python extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
    - [Komodo IDE](https://www.activestate.com/komodo-ide/python-editor)

2. [Prepare and configure the Arduino YÚN device](setup-arduino.md)

3. [Create an Amazon Web Services (AWS) IoT Thing](setup-aws-iot.md)

4. [Create an Alexa Smart Home Skill](setup-alexa-skill-create.md)

5. [Create an Amazon Web Services (AWS) Lambda for the Alexa Smart Home Skill](setup-alexa-lambda.md)

6. [Configure the Alexa Smart Home Skill](setup-alexa-skill-configure.md)

7. [Copy the Python code to the Arduino](setup-arduino-python.md)

8. [Deploy the INO code to the Arduino](setup-arduino-ino.md)

9. Test the integration

    When everything is running, you should be able to send commands to Alexa like the following:
    - Alexa, turn on sample light
    - Alexa, turn off sample light
    - Alexa, set sample light to red
    - Alexa, set sample light to green
    - Alexa, set sample light to blue
    - Alexa, set sample light to white
    - Alexa, set sample light to warm white
    - Alexa, set sample light to cool white
    - Alexa, set sample light to 50%
    - Alexa, dim sample light
    etc.
    
### Troubleshooting
If you encounter any errors or the sample does not appear to run correctly:

- Check that the .ino sketch and .py script are running on the Arduino YÚN device
- Check the CloudWatch logs for details


