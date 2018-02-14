### Create an Amazon Web Services (AWS) Lambda for the Alexa Smart Home Skill

#### Package the Lambda Code
To package the lambda code, the files in the _alexa_ source directory will need to be collected into a zip file.

- Zip all the .py and .json files in the _alexa_ directory into the root of a zip file named ```package.zip```.
> The package.zip file should not include the /alexa directory but only the files themselves.

#### Create the Alexa Smart Home Lambda function
Go to AWS Lambda console at [https://console.aws.amazon.com/lambda/home](https://console.aws.amazon.com/lambda/home).

1. Select **Functions** from the left menu.
2. Click the **Create function** button.
3. From the _Create function_ page, select **Author from Scratch**.
4. In the name of the function, set ```sampleArduinoLight```.
5. Change the runtime to **Python 3.6**.
6. Select an _Existing role_ of **lambda_basic_execution role** if available. 

    > If not available, you will need create a role with Lambda and Cloudwatch permissions. For more information, review [Manage Permissions: Using an IAM Role (Execution Role)](https://docs.aws.amazon.com/lambda/latest/dg/intro-permission-model.html#lambda-intro-execution-role).

7. In the _sampleArduinoLight_ configuration and within the **Designer** click on the **Alexa Smart Home** trigger to add it to the function.

8. Further down the page in the _Configure triggers_ section, paste the **Alexa Application Id** created earlier.
9. Make sure **Enable trigger** is checked.
10. Click the **Add** button to add the Trigger.
11. Click the **Save** button at the top to save the function.
12. Within the Designer, select the _sampleArduinoLight_ function and select **Upload a Zip file** from the _Code entry type_ of the _Function code_ section.
13. Click the **Upload** button and then select the ```package.zip``` file created earlier.
14. Click the **Save** button at the top to save the function.
15. At the top of the page, note the ARN of the function. This value will be unique and look like the following: ```arn:aws:lambda:us-east-1:############:function:sampleArduinoLight```. This identifier will be used to configure the Alexa Smart Home skill.



[Continue with the Setup](setup.md)