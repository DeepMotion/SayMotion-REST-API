# **Saymotion REST API**


## Revisions


# _Beta v1.0.0_

Initial rest APIs


# _Beta v1.1.0_

/account/creditBalance (introducing feature limits)

/job/process (changes due to variant & inpainting generation)

/job/list (changes due to variant & inpainting generation and also multi mp4 downloads)

/job/download (changes due to variant & inpainting generation)

The SayMotion REST API lets you convert text prompts into 3D animations without having to use the Saymotion [Web Portal](https://saymotion.ai/). It can be used from web, mobile or desktop apps.


# Authentication

The SayMotion  REST API uses basic **HTTP Authentication** to keep your requests and data secure. To use the API you will need a **Client ID** and a **Client Secret **which are provided by DeepMotion. If you do not have these please contact DeepMotion Support or your sales representative.

To retrieve your API access token you need to add the following Authorization header to your token request:


```
Authorization: Basic Base64(<clientId>:<clientSecret>)
```


where the value of `&lt;clientId>:&lt;clientSecret>` is **base 64** encoded.  For Example, if your Client ID is `1a2b` and your client Secret is `3c4d` then your authorization header should look like this: 


```
Authorization: Basic MWEyYjozYzRk
```


where `MWEyYjozYzRk` is the base64 encoded value of `1a2b:3c4d.`


# API Endpoints

All SayMotion API requests must be made against the following base URL using the HTTPS protocol and port:


```
Production Environment: 	(Contact DeepMotion)
```


**For using our API from browser javascript** locally (to avoid CORS error), please send request from the origin below:

[http://localhost](http://localhost:8080/)

For production deployment, please let us know your production url (scheme, host, port), so that we can configure our CORS setting accordingly.


# API Reference

Account APIs

**API 1: Authentication & getting Access Token**


<table>
  <tr>
   <td><strong>Desc</strong>
   </td>
   <td>Authenticate client credentials and returns a time limited session cookie to be used in the subsequent REST API calls. After the session expires, this API needs to be called again to get a new session cookie. Please use this api from the server side to stay secure for web applications and you can use the returned session cookie in other API calls even from the client side.
   </td>
  </tr>
  <tr>
   <td><strong>Method + URI</strong>
   </td>
   <td>GET {host}/account/v1/auth
   </td>
  </tr>
  <tr>
   <td><strong>Header(s)</strong>
   </td>
   <td>Authorization: Basic Base64(&lt;clientId>:&lt;clientSecret>)
   </td>
  </tr>
  <tr>
   <td><strong>Request </strong>
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td><strong>Response</strong>
   </td>
   <td>Sample Response Header:
<p>
set-cookie: dmsess=s%3AEsF23MoyDEq7tTWQM8KfA_wjKkSrOFwU.2fjJTfDP%2FT2BeA5DFenwOH4t8XzqZsbSc6M2mZwS%2BWg; 
<p>
Domain=.deepmotion.com; Path=/; Expires=Mon, 03 Aug 2020 13:36:26 GMT; HttpOnly
<p>
(Note:<strong> dmsess </strong>is the session cookie. This cookie needs to be sent in all subsequent REST API calls.
<p>
Sample Request Header for other API calls:
<p>
cookie:dmsess=s%3AEsF23MoyDEq7tTWQM8KfA_wjKkSrOFwU.2fjJTfDP%2FT2BeA5DFenwOH4t8XzqZsbSc6M2mZwS%2BWg)
   </td>
  </tr>
</table>


**API 2: Credit Balance**


<table>
  <tr>
   <td><strong>Desc</strong>
   </td>
   <td>Retrieves Credit Balance for an user
   </td>
  </tr>
  <tr>
   <td><strong>Method + URI</strong>
   </td>
   <td>GET {host}/account/v1/creditBalance
   </td>
  </tr>
  <tr>
   <td><strong>Header(s)</strong>
   </td>
   <td>cookie:dmsess=&lt;cookie-value-returned-from-authentication-api>
   </td>
  </tr>
  <tr>
   <td><strong>Request</strong>
   </td>
   <td>n/a
   </td>
  </tr>
  <tr>
   <td><strong>Response</strong>
   </td>
   <td>JSON object:
<p>
{"credits":&lt;value>,"subscription":{"name":&lt;value>,"credits":&lt;value>,"featureLimits":{"maxVariantsGeneration":&lt;value>},"currentPeriod":{"start":&lt;value>,"end":&lt;value>}}}
   </td>
  </tr>
</table>


Job APIs

**API 1: Start Processing**


<table>
  <tr>
   <td><strong>Desc</strong>
   </td>
   <td>Start processing text to motion OR rendering a previously generated animation
   </td>
  </tr>
  <tr>
   <td><strong>Method + URI</strong>
   </td>
   <td>POST {host}/job/v1/process/processor
   </td>
  </tr>
  <tr>
   <td><strong>Header(s)</strong>
   </td>
   <td>cookie:dmsess=&lt;cookie-value-returned-from-authentication-api>
   </td>
  </tr>
  <tr>
   <td><strong>Request</strong>
   </td>
   <td>POST body should include a JSON object:
<p>
{
<p>
  “params": [&lt;params>, ...]
<p>
}.
<p>
 
<p>
&lt;processor> specifies which processor to use to process the job, must be one of the following:

<table>
  <tr>
   <td><strong>Processor Id</strong>
   </td>
   <td><strong>Description</strong>
   </td>
  </tr>
  <tr>
   <td>text2motion
   </td>
   <td>textPrompt to animation generator
   </td>
  </tr>
  <tr>
   <td>render
   </td>
   <td>Renders an animation to video
   </td>
  </tr>
</table>


&lt;params> specifies additional parameters that will be passed to the specified processor.

For the **text2motion **processor, here are the parameters for a regular job.

"params":

 [

 “prompt=&lt;value>”,

 "model=&lt;value>”,

 "requestedAnimationDuration=&lt;value>”,

 “dis=&lt;value>”,

 “footLockingMode=&lt;value>”,

“poseFilteringStrength=&lt;value>”,

“rootAtOrigin=&lt;value>”

 ]

And here are the additional parameters for an inpainting job

"params":

 [

 “t2m_rid=&lt;value>”,

 “variant_id=&lt;value>”,

 “inPaintingRequest={ “prompt” :&lt;value>,  “intervals” : [ { “start” :&lt;value>, “end”:&lt;value> } ] }”

 ]

**prompt**

A detailed text prompt to generate motion with. For inpainting jobs, the prompt parameter should be included inside the inPaintingRequest parameter, instead of as a standalone parameter in a regular job.

**model**

The 3d model used for showcasing the generated motion/animation

**dis (optional)**

This parameter influences motion generation to improve it in some cases like inter body parts penetration etc, but may cause side effects in animation quality sometimes. By default simulation is turned on. Use **dis=s** to turn off the simulation.

**footLockingMode  (optional)**



* This parameter value can be one of the below:
    * **auto** : default mode, automatic switching between locking and gliding modes of the foot, recommended for general cases
    * **always** :  forced foot locking all the time. only used when Auto mode can not remove all the foot gliding unsired
    * **never** : forced to disable foot locking and character grounding. used when the motion is completely in the air or in the water and therefore neither foot locking nor character grounding is needed.
    * **grounding** : forced disabling foot locking, however character is still grounded. Only used when Auto mode prevents the desired foot gliding (i.e. during shuffling dances) in the motion or locks the foot for too long on the ground during fast and short foot/ground contacts (i.e. during sprints or jumps.)

**poseFilteringStrength (optional)**



* Applies an advanced AI filter that helps remove jitter and produce smoother animations though may result in lower animation accuracy for certain frames or sequences
* Default value is 0.0 and range is 0.0 - 1.0 

**rootAtOrigin (optional)**



* Place a root joint at the origin of the output character. This is helpful in some cases, for example, for UE4 retargeting.
* Default value is 0 and value can be either 0 or 1

**requestedAnimationDuration (optional)**



* Float, request animation generation duration in seconds

**t2m_rid**



* It is a previous text2motion job request id from which to generate inpainting jobs

**variant_id**



* It is a specific variant animation id from the above previously generated text2motion job

**inPaintingRequest**



* A json string, containing inpainting prompt and intervals in frame numbers.

For the **render **processor, here are the parameters.

Only two required parameters are **t2m_rid** which is a previous text2motion job request id  & **variant_id** which is a specific variant animation from the above previously generated text2motion job. Other optional parameters are below:

*To replace the default background with a solid color (for green screening etc.)

**bgColor=0,177,64,0**  (RGBA color code in the range of 0-255 for each channel, please note, the last channel (alpha) value is not in effect )

*To set a studio like 3d background with a solid color tint

**backdrop=studio**

**bgColor=0,177,64,0 **

Also, List of supported 2D backdrops:



* Checker_Cloudscape
* Golden_Age_Glitz
* Inferno_Stage
* Jungle_Grove
* Mystic_Brick
* Mystic_Concrete
* Rainbow_Spotlight
* Red_Carpet
* Retro_Revue
* Sakura_Dreamscape
* Spotlit_Stage
* Timbered_Retreat
* Urban_Rooftop

*To enable character shadow

**shadow=1 ** (not applicable for 2D backdrop)

***camMode**

values are below. Default is 0

0 (Cinematic) The character is kept in the center of the frame

1 (Fixed) Camera will stay fixed relative to the background

2 (Face) Camera keeps the torso and face in the center of frame

***camHorizontalAngle**

Camera horizontal angle in degrees, where zero means forward camera



* Default value is 0 and range is -90 - +90
   </td>
  </tr>
  <tr>
   <td>
**Response**

   </td>
   <td>JSON object:

{

  "rid": &lt;request id>

}

   </td>
  </tr>
</table>


**API 2: Poll for Job Status**


<table>
  <tr>
   <td><strong>Desc</strong>
   </td>
   <td>Polls for real-time status of a given processing job
   </td>
  </tr>
  <tr>
   <td><strong>Method + URI</strong>
   </td>
   <td>GET {host}/job/v1/status/rid
<p>
GET {host}/job/v1/status/rid1,rid2,..,rid
   </td>
  </tr>
  <tr>
   <td><strong>Header(s)</strong>
   </td>
   <td>cookie:dmsess=&lt;cookie-value-returned-from-authentication-api>
   </td>
  </tr>
  <tr>
   <td><strong>Request</strong>
   </td>
   <td>Clients can request the current status of previously submitted processing requests (API3).
<p>
Use comma (‘,’) to separate multiple request ids if retrieving status for more than 1 request.
   </td>
  </tr>
  <tr>
   <td><strong>Response</strong>
   </td>
   <td>JSON object:
<p>
{
<p>
  "count": &lt;number of records in status array>,
<p>
  "status": [
<p>
     &lt;status>,
<p>
     … …
<p>
  ]
<p>
}
<p>
Each element in status array is a JSON object:
<p>
{
<p>
  "rid": &lt;request id>,
<p>
  "status": &lt;status name>,
<p>
  "details": &lt;status details, see below>,
<p>
  “positionInQueue”: &lt;position in the queue for only PROGRESS status>
<p>
}
<p>
&lt;status name> is one of the following <strong>case sensitive</strong> values:

<table>
  <tr>
   <td><strong>Status Name</strong>
   </td>
   <td><strong>Description</strong>
   </td>
  </tr>
  <tr>
   <td>PROGRESS
   </td>
   <td>Request is still being processed
   </td>
  </tr>
  <tr>
   <td>SUCCESS
   </td>
   <td>Request is processed successfully
   </td>
  </tr>
  <tr>
   <td>FAILURE
   </td>
   <td>Request has failed
   </td>
  </tr>
</table>


&lt;status details> for PROGRESS:

{

  “step”: &lt;current step>,

  “total”: &lt;expected total number of steps>

}

&lt;status details> for SUCCESS:

{

  “In”: &lt;original video file>,

  “out”: &lt;processed video file>

}

&lt;status details> for RETRY and FAILURE include last error message. Currently the format is:

{

  “exc_message”: &lt;exception message, if any>,

  “exc_type”: &lt;exception type, if any>

}

But please note the format may change if we decide to mask error information (or pass more information) to client applications.

   </td>
  </tr>
</table>


**API 3: Get Download URLs**


<table>
  <tr>
   <td><strong>Desc</strong>
   </td>
   <td>Get download URLs for the specified request ids
   </td>
  </tr>
  <tr>
   <td><strong>Method + URI</strong>
   </td>
   <td>GET {host}/job/v1/download/rid?variant_id=1
<p>
GET {host}/job/v1//download/rid1,rid2,...,rid?variant_id=2,3,...,n
   </td>
  </tr>
  <tr>
   <td><strong>Header(s)</strong>
   </td>
   <td>cookie:dmsess=&lt;cookie-value-returned-from-authentication-api>
   </td>
  </tr>
  <tr>
   <td><strong>Request</strong>
   </td>
   <td>Clients can request download URLs for finished processing requests.
<p>
Use comma (‘,’) to separate request ids if retrieving download URLs for multiple processing requests.
<p>
A query parameter called <strong>variant_id </strong>to be able to download specific variant animation related resources. Use comma (‘,’) to separate variant_id values which correspond to individual rid of multiple job requests
   </td>
  </tr>
  <tr>
   <td><strong>Response</strong>
   </td>
   <td>JSON object:
<p>
{
<p>
  “count”: &lt;number of records in links array>,
<p>
  “links”: [
<p>
    &lt;link>,
<p>
    … ...
<p>
  ]
<p>
}
<p>
Each element in links array is a JSON object:
<p>
{
<p>
  “rid”: &lt;request id>,
<p>
  “parameters”: &lt;input params of the job>,
<p>
  “renderJobList” (available only for text2motion jobs):&lt;value>
<p>
  “variantDownloadStatus”: &lt;boolean flag, false when variant id is wrong or user doesn’t has sufficient balance to download this variant data>
<p>
  “urls”: [
<p>
   {
<p>
    “name”: &lt;name of the downloadable item>
<p>
    “files”: &lt;links of the files by extension> [
<p>
     { &lt;file type>: &lt;URL to download the corresponding file>},
<p>
     {&lt;file type>: &lt;URL to download the corresponding file>}
<p>
     ]
<p>
   }
<p>
  ]
<p>
}
<p>
Please note that if the specified request has not finished yet or has failed, the response will not include any download urls, and the link object will look like:
<p>
{
<p>
  “rid”: “1234567890”
<p>
}
   </td>
  </tr>
</table>


**API 4: List All Video Processing requests by Status & processor**


<table>
  <tr>
   <td><strong>Desc</strong>
   </td>
   <td>List past and current request ids
<p>
Note: failed jobs and old jobs may be removed by system after a predefined retention period
   </td>
  </tr>
  <tr>
   <td><strong>Method + URI</strong>
   </td>
   <td>GET {host}/job/v1/list
<p>
GET {host}/job/v1/list/status1,...,status/processor
   </td>
  </tr>
  <tr>
   <td><strong>Header(s)</strong>
   </td>
   <td>cookie:dmsess=&lt;cookie-value-returned-from-authentication-api>
   </td>
  </tr>
  <tr>
   <td><strong>Request</strong>
   </td>
   <td>Client can request to get list of existing request ids of current user
<p>
Client can specify one or multiple status value(s) along with processor id to retrieve only request ids with the same status value(s). For example, GET /list/PROGRESS/text2motion will only return list of text2motion requests that are still being processed
   </td>
  </tr>
  <tr>
   <td><strong>Response</strong>
   </td>
   <td>JSON object:
<p>
{
<p>
   "count": &lt;number of records in the rids array>,
<p>
  "list": [
<p>
    {
<p>
      "rid": &lt;job request id>,
<p>
      "processingInfo":&lt;detail timing of the processing>,
<p>
      "processor":&lt;processor id>,
<p>
      "parameters":&lt;job input parameters>,
<p>
      “variants” (available only for text2motion jobs): &lt;{“variant_id”:{“download”:&lt;download flag>}}>
<p>
      “chargedAmount”: &lt;credits used for this job>
<p>
      "status": &lt;status of the job>,
<p>
      "ctime": &lt;creation time,milliseconds since epoch>,
<p>
      "mtime": &lt;last modification time, milliseconds since epoch>
<p>
    },
<p>
    ... ...
<p>
  ]
<p>
}
   </td>
  </tr>
</table>


**API 5: Cancel progressing job**


<table>
  <tr>
   <td><strong>Desc</strong>
   </td>
   <td>Cancel job for the specified request id
   </td>
  </tr>
  <tr>
   <td><strong>Method + URI</strong>
   </td>
   <td>GET {host}/job/v1/cancel/rid
   </td>
  </tr>
  <tr>
   <td><strong>Header(s)</strong>
   </td>
   <td>cookie:dmsess=&lt;cookie-value-returned-from-authentication-api>
   </td>
  </tr>
  <tr>
   <td><strong>Request</strong>
   </td>
   <td>Clients can cancel in progress request/job.
   </td>
  </tr>
  <tr>
   <td><strong>Response</strong>
   </td>
   <td>JSON object:
<p>
{
<p>
“result”: true
<p>
 }
   </td>
  </tr>
</table>



# Custom Character APIs

**API 1: Model Upload Url**


<table>
  <tr>
   <td><strong>Desc</strong>
   </td>
   <td>Retrieves signed urls to upload 3d model data(fbx, glb, gltf, or vrm format) and thumbnail(preferably png format)
   </td>
  </tr>
  <tr>
   <td><strong>Method + URI</strong>
   </td>
   <td>GET {host}/character/v1/getModelUploadUrl
   </td>
  </tr>
  <tr>
   <td><strong>Header(s)</strong>
   </td>
   <td>cookie:dmsess=&lt;cookie-value-returned-from-authentication-api>
   </td>
  </tr>
  <tr>
   <td><strong>Request</strong>
   </td>
   <td>Query parameters:
<p>
&lt;name>: base name of the files (without extension) (optional)
<p>
&lt;modelExt>: file extension of the model file. Example: fbx  (optional)
<p>
&lt;thumbExt>: file extension of the thumb file. Example: jpg (optional)
<p>
&lt;resumable>: 0 or 1(default) returns resumable or regular signed url (optional)
   </td>
  </tr>
  <tr>
   <td><strong>Response</strong>
   </td>
   <td>JSON object:
<p>
{
<p>
  “modelUrl”: signed url
<p>
  “thumbUrl”: signed url
<p>
}
<p>
After retrieving the urls, actual model & thumbnail upload are required to that storage urls. If ’resumable’ option is set in the request,  we need one POST and one subsequent PUT request for each signed url, otherwise a single PUT request will do the job per url.
<p>
POST request to url:
<p>
&lt;x-goog-resumable>: start (set in the request header)
<p>
&lt;location>: resumable url (set in the response header by server)
<p>
PUT request to resumable url location/url:
<p>
attach raw bytes of the model or thumbnail file in the request body.
   </td>
  </tr>
</table>


**API 2: Store Model**


<table>
  <tr>
   <td><strong>Desc</strong>
   </td>
   <td>Store the asset paths returned from getModelUploadUrl in database
   </td>
  </tr>
  <tr>
   <td><strong>Method + URI</strong>
   </td>
   <td>POST {host}/character/v1/storeModel
   </td>
  </tr>
  <tr>
   <td><strong>Header(s)</strong>
   </td>
   <td>cookie:dmsess=&lt;cookie-value-returned-from-authentication-api>
   </td>
  </tr>
  <tr>
   <td><strong>Request</strong>
   </td>
   <td>Body parameters:
<p>
&lt;modelUrl>: model url returned from API 1 (optional if  &lt;modelId> is provided)
<p>
&lt;modelName>: model  name (optional)
<p>
&lt;thumbUrl>: thumbnail url returned from API 1 (optional)
<p>
&lt;modelId>: model id to update existing model info (name or thumb) (optional if  &lt;modelUrl> is provided)
<p>
&lt;createThumb>: 0 (default) or 1, indicate if the thumbnail of the model needs to be generated (optional)
   </td>
  </tr>
  <tr>
   <td><strong>Response</strong>
   </td>
   <td>JSON object:
<p>
{
<p>
  “modelId”: &lt;Unique model id that can be passed to text2motion process API>,
<p>
  “faceDataType”:&lt;if the model supports facial rig>,
<p>
  “handDataType”:&lt;if the model supports hand/finger rig>
<p>
}
   </td>
  </tr>
</table>


**API 3: List Models**


<table>
  <tr>
   <td><strong>Desc</strong>
   </td>
   <td>List models based on specific query or without
   </td>
  </tr>
  <tr>
   <td><strong>Method + URI</strong>
   </td>
   <td>GET {host}/character/v1/listModels
   </td>
  </tr>
  <tr>
   <td><strong>Header(s)</strong>
   </td>
   <td>cookie:dmsess=&lt;cookie-value-returned-from-authentication-api>
   </td>
  </tr>
  <tr>
   <td><strong>Request</strong>
   </td>
   <td>Query parameters:
<p>
&lt;modelId>: existing model id (optional)
<p>
&lt;searchToken>: for example search by model name (optional)
<p>
&lt;stockModel>: = When this parameter is supplied, all stock models (including deepmotion & roblox) will return in api response along with the account's custom models. Beside that, each model details now include a platform field which can be one of the below values : custom, deepmotion, roblox . (optional)
   </td>
  </tr>
  <tr>
   <td><strong>Response</strong>
   </td>
   <td>JSON object:
<p>
[
<p>
 {
<p>
   “Id: Unique model id that can be passed to video process API
<p>
   “name”: name of the model
<p>
   “thumb”: url of the thumbnail if exist
<p>
   “glb”: url of glb format of the character
<p>
   “rigId”: rigTemplate id with which this model is associated with
<p>
   “ctime”: creation timestamp
<p>
   “mtime”: modification timestamp
<p>
   “platform”: platform of the model 
<p>
 }
<p>
]
   </td>
  </tr>
  <tr>
   <td>
   </td>
   <td>
   </td>
  </tr>
</table>


**API 4: Delete Model**


<table>
  <tr>
   <td><strong>Desc</strong>
   </td>
   <td>Delete model with specific model ID
   </td>
  </tr>
  <tr>
   <td><strong>Method + URI</strong>
   </td>
   <td>DELETE {host}/character/v1/deleteModel/&lt;model ID>
   </td>
  </tr>
  <tr>
   <td><strong>Header(s)</strong>
   </td>
   <td>cookie:dmsess=&lt;cookie-value-returned-from-authentication-api>
   </td>
  </tr>
  <tr>
   <td><strong>Request</strong>
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td><strong>Response</strong>
   </td>
   <td>JSON object:
<p>
{
<p>
  “count”: number of models that have been deleted. Currently only one model can be deleted at a time.
<p>
}
   </td>
  </tr>
</table>



# Saymotion Restful API Error Codes (Updates as we add more features)


<table>
  <tr>
   <td>Error Code
   </td>
   <td>Meaning
   </td>
  </tr>
  <tr>
   <td>101
   </td>
   <td>Not enough credit
   </td>
  </tr>
  <tr>
   <td>498
   </td>
   <td>Unknown pipeline error
   </td>
  </tr>
  <tr>
   <td>494
   </td>
   <td>Invalid pipeline Input
   </td>
  </tr>
  <tr>
   <td>501
   </td>
   <td>Error while generating motion
   </td>
  </tr>
  <tr>
   <td>502
   </td>
   <td>Error parsing motion generation parameters
   </td>
  </tr>
  <tr>
   <td>599
   </td>
   <td>Motion generation timeout
   </td>
  </tr>
  <tr>
   <td>603
   </td>
   <td>Error processing pose tracking parameters
   </td>
  </tr>
  <tr>
   <td>604
   </td>
   <td>Error loading animation data for pose tracking
   </td>
  </tr>
  <tr>
   <td>605
   </td>
   <td>Physics Filter is incompatible with used custom character
   </td>
  </tr>
  <tr>
   <td>607
   </td>
   <td>Error while processing the body tracking
   </td>
  </tr>
  <tr>
   <td>610
   </td>
   <td>Error saving pose tracking intermediate results
   </td>
  </tr>
  <tr>
   <td>699
   </td>
   <td>Pose tracking timeout
   </td>
  </tr>
  <tr>
   <td>703
   </td>
   <td>Error processing pose correction parameters
   </td>
  </tr>
  <tr>
   <td>704
   </td>
   <td>Error loading the character animation assets for pose corrections
   </td>
  </tr>
  <tr>
   <td>710
   </td>
   <td>Error saving pose correction intermediate results
   </td>
  </tr>
  <tr>
   <td>799
   </td>
   <td>Pose correction timeout
   </td>
  </tr>
  <tr>
   <td>803
   </td>
   <td>Error processing bvh exporter parameters
   </td>
  </tr>
  <tr>
   <td>804
   </td>
   <td>Error loading the character animation assets for bvh exporting
   </td>
  </tr>
  <tr>
   <td>810
   </td>
   <td>Error saving bvh results
   </td>
  </tr>
  <tr>
   <td>899
   </td>
   <td>Bvh exporting timeout
   </td>
  </tr>
  <tr>
   <td>901
   </td>
   <td>Error loading the mesh of the custom character
   </td>
  </tr>
  <tr>
   <td>902
   </td>
   <td>Error loading the BVH custom character
   </td>
  </tr>
  <tr>
   <td>903
   </td>
   <td>Error copying animations onto the custom character
   </td>
  </tr>
  <tr>
   <td>904
   </td>
   <td>Error exporting animations for the custom character
   </td>
  </tr>
  <tr>
   <td>905
   </td>
   <td>Custom character doesn’t include skinned mesh information
   </td>
  </tr>
  <tr>
   <td>906
   </td>
   <td>More than half of the required blendshapes are missing
   </td>
  </tr>
  <tr>
   <td>907
   </td>
   <td>Error loading facial definition for the custom character
   </td>
  </tr>
  <tr>
   <td>908
   </td>
   <td>Error loading facial tracking data
   </td>
  </tr>
  <tr>
   <td>909
   </td>
   <td>Error loading the metadata of the custom character
   </td>
  </tr>
  <tr>
   <td>999
   </td>
   <td>Animation baking timeout
   </td>
  </tr>
  <tr>
   <td>1101
   </td>
   <td>Process stuck
   </td>
  </tr>
  <tr>
   <td>1102
   </td>
   <td>Invalid input parameter
   </td>
  </tr>
  <tr>
   <td>1105
   </td>
   <td>Failed to load input character
   </td>
  </tr>
  <tr>
   <td>1106
   </td>
   <td>Failed to attach animation to character
   </td>
  </tr>
  <tr>
   <td>1107
   </td>
   <td>Failed to configure backdrop
   </td>
  </tr>
</table>