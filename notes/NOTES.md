see: https://developer.amazon.com/docs/adm/obtain-credentials.html

0) Generate APK keystore & App Key (if not already done)

0) Fetch out the MD5 and SHA-256 Keys:
    Unfortunately, later versions of the keytool do NOT display the MD5 value, even though AWS wants it.
    Instead, inside of Android Studio:
    ```
    click on the Gradle tab,
    > <Your Project Name>
     > Tasks
       > Android
         > signingReport
    ```
    This will display the MD5 value

    `keytool -list -v -keystore YourKeystore.jks` will display the SHA256 value.

0) Submit info and generate new API key. Show key and copy API key data.

0) Create app credentials at: https://developer.amazon.com/apps-and-games?
    * register the app
    * Create security profile
    (copy out info)

    <table>
    <tr><th>Security Profile Name</th><td>ADMPushDemo profile</td></tr> 
    <tr><th>Security Profile Description</th><td>ADMPushDemo Messaging security profile</td></tr> 
    <tr><th>Security Profile ID</th><td>amzn1.application.0e7299346d984630b9cc6211d0c23e15 </td></tr>
    <tr><th>Client ID</th><td>amzn1.application-oa2-client.1d2f79cbbd9e45d48c76c95db8738c4c </td></tr>
    <tr><th>Client Secret</th><td>559dac53757a571d2fee78e5fcb223293aaf4e39b4a0d9f69924dc91149f95c5 </td></tr>
    </table>
    
0) Copy the API Key into `${PROJECT_DIR}/src/main/assets/api_key.txt`
***NOTE***: You ***will not*** be able to test this application in the emulator. The provided
jar file contains only stub references. The actual jar file is only available on amazon devices.

NOTE:: It is possible that the CERT.RSA key used to sign the app may change slightly. If 
you get an error like "INVALID_SENDER" yet the `assets/api_key.txt` is included, check that
the CERT.RSA SHA256 key matches what you've registered with Amazon. A new key may need to be
generated. 

Remember, your app key is stored usually stored in the *.keystore file (if using Android Studio) 