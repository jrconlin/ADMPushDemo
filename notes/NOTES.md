see: https://developer.amazon.com/docs/adm/obtain-credentials.html

# Server Requirements
0) Generate APK keystore & App Key (if not already done)

0) Fetch out the MD5 and SHA-256 Keys:

    Unfortunately, later versions of the keytool do NOT display the MD5 value, even though AWS wants it.
    Instead, you can fetch the MD5 from inside of Android Studio:
    ```
    click on the Gradle tab,
    > <Your Project Name>
     > Tasks
       > Android
         > signingReport
    ```
    To display the SHA256 value:

    `keytool -list -v -keystore YourKeystore.jks`
    
    ***Note***: It is possible that the CERT.RSA key used to sign the app may change slightly. If 
                you get an error like "INVALID_SENDER" yet the `assets/api_key.txt` is included, check that
                the CERT.RSA SHA256 key matches what you've registered with Amazon. A new key may need to be
                generated. 
                
0) Submit info and generate new API key. Show key and copy API key data.

0) Create app credentials at: https://developer.amazon.com/apps-and-games?
    * register the app
    * Create security profile
    (copy out info)

    For instance:
    <table>
    <tr><th>Security Profile Name</th><td>ADMPushDemo profile</td></tr> 
    <tr><th>Security Profile Description</th><td>ADMPushDemo Messaging security profile</td></tr> 
    <tr><th>Security Profile ID</th><td>amzn1.application.0e729... </td></tr>
    <tr><th>Client ID</th><td>amzn1.application-oa2-client.1d2f... </td></tr>
    <tr><th>Client Secret</th><td>559d... </td></tr>
    </table>
    
0) Copy the API Key into `${PROJECT_DIR}/src/main/assets/api_key.txt`
***NOTE***: You ***will not*** be able to test this application in the emulator. The provided
jar file contains only stub references. The actual jar file is only available on amazon devices.


# Client Requirements

* Add the API Key (from above) to  `./assets/api_key.txt`.
    * In app.iml add: 
    ```aidl
    android {
        ...
        sourceSets { main { assets.srcDir = ['src/main/assets', 'src/main/assets/'] } }
        ...
    }
    ```
    
* Add the `amazon-device-messaging-*.jar` as a `compileOnly` dependency
    * In app.iml add:
    ```aidl
    ...
    dependencies {
       compileOnly files('libs/amazon-device-messaging-1.0.1.jar')
    }  
    ```
    
* [Register application with ADM](https://developer.amazon.com/docs/adm/integrate-your-app.html):

  While demo calls registration in the `Activity.onCreate()` override, it does not appear that this
  is strongly enforced. The call should be made in the applications main activity. In any case, registration is fairly straight-forward:
  
  ```aidl
    final ADM adm = new ADM(Context: this);
    if (adm.isSupported()){
        if(adm.getRegistrationId() == null){
            adm.startRegister();
        }
        Log.i("register", "Registration ID:" + adm.getRegistrationId());
    }
  ``` 
  
  This may throw an "INVALID_SENDER" exception in several cases:
  0) If the `api_key.txt` asset file cannot be found
  0) If the file cannot be properly parsed (note, remove whitespace. It's a JWT object)
  0) If the app package, CERT.RSA key signatures, or other information in the API key does not match the information stored in the key registration block.

The registration token is 1536 octets long. 

You can send it to the PushServer registration endpoint as:

  ```
  POST https://updates.push.services.mozilla.com/v1/adm/<profile_name>/registration
  
  {"token":<registration_token_id>}
  
  ```
  where:
  
  * *profile_name* is one of the Security Profiles registered with the server. (Please send the 
  profile name, Client ID and Client Secret before using this key. Profile Name should be a short, 
  URL safe identifier, like "prod" or "dev". It may be the Security Profile ID if desired, but
  that might be a bit long.
  
  * *registration_token_id* is the returned value from ADM().getRegistrationId().
  
 ## Suggestions:
 * It appears that applications simply get the registrationId when needed. I have no idea if 
 this value changes at any point, but if it does, your application should [update the value on 
 the server](http://autopush.readthedocs.io/en/latest/http.html#token-updates). If not, there's 
 a very good chance that the server may no longer be able to send messages.
 
 * The Amazon docs are fairly good, but tend to leave out a fair bit of detail. They also appear
 to lag behind a fair bit. I apologize that the demo is not in Kotlin, but I was unable to get
 that bit working easily with the provided demo app. I don't expect there to be much trouble for 
 more experienced devs to move things over.
 