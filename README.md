# Mox : stsorgsync

Integration between OS2MO and StsOrgSync

StsOrgSync ([https://github.com/Gentofte/STSOrgSync](https://github.com/Gentofte/STSOrgSync)) is a middleware meant to make it easier to 
insert / upgrade organizational units and users into STS organization

This small module exports OS2MO Employees and Organizational units along with selected relations, a subset of the available addresses, itsystems and engagements to STS organization via StsOrtgSync.

Apart from the configuration for this module, which is rather small, care must be taken to follow the steps outlined in the installation manual for StsOrgSync, 
the current version being [this](https://github.com/Gentofte/STSOrgSync/raw/master/Documentation/Installation%20Guide.docx)

The most important step is to get access to Production and Test-instances of STS-Organization on serviceplatformen.

The configuration of this module is quite simple and is done using a configuration file which is found like this:

* location is specifed in environment-variable *MOX_MO_CONFIG*
* location is 'settings.ini' in current working directory
* location is 'settings.ini' next to the file 'config.py'


The configuration looks like this:

    [settings]

    ; log level set this to a numeric representation of a log level - 10 is debug.
    MOX_LOG_LEVEL = 10 

    ; log file - set this to blank to have log in stderr, otherwise this must be a file name. 
    MOX_LOG_FILE =

    ; os2mo-service url - this is the full url to os2mo-service - it must end in '/service'.
    OS2MO_SERVICE_URL = 

    ; os2mo saml token - if You are running an authenticated OS2MO, You must use this access token.
    OS2MO_SAML_TOKEN =

    ; os2mo org uuid - leave it blank to query it from server. 
    OS2MO_ORG_UUID = 
    
    ; os2mo ca bundle - 'true' means use the built in ca-bundle, 'false' or blank means dont use any
    ; otherwise it is interpreted as a filename pointing to the ca certs.
    OS2MO_CA_BUNDLE = true

    ; stsorgsync api url - this is the url to the stsorgsync instance - it will typically end with '/api/v1_1' or similar 
    STSORGSYNC_API_URL = http://some-stsorgsync-url/api/v1_1

    ; stsorgsync ca bundle - 'true' means use the built in ca-bundle, 'false' or blank means dont use any
    ; otherwise it is interpreted as a filename pointing to the ca certs.
    STSORGSYNC_CA_BUNDLE = true

A typical logfile (with loglevel 20) should look somethat like this:

    INFO 2019-05-03 12:01:19,485 mox_stsorgsync mox_stsorgsync starting
    INFO 2019-05-03 12:01:19,567 mox_stsorgsync sync_stsorgsync_orgunits starting
    INFO 2019-05-03 12:01:19,567 mox_stsorgsync sync_stsorgsync_orgunits getting all organisational units from os2mo
    INFO 2019-05-03 12:01:20,245 mox_stsorgsync sync_stsorgsync_orgunits getting all organisational units from stsorgsync
    INFO 2019-05-03 12:01:20,683 mox_stsorgsync sync_stsorgsync_orgunits deleting organisational units from stsorgsync if deleted in os2mo
    INFO 2019-05-03 12:01:20,683 mox_stsorgsync sync_stsorgsync_orgunits upserting organisational units in stsorgsync
    INFO 2019-05-03 12:01:21,973 mox_stsorgsync upsert orgunit aa0d5012-4320-4715-bb74-f087befefaa8
    ...
    INFO 2019-05-03 12:01:23,181 mox_stsorgsync upsert orgunit cf8cfc65-f6a6-4ca8-9812-f50322cc0ec9
    INFO 2019-05-03 12:01:44,706 mox_stsorgsync sync_stsorgsync_orgunits done
    INFO 2019-05-03 12:02:44,706 mox_stsorgsync sync_stsorgsync_users starting
    INFO 2019-05-03 12:02:44,706 mox_stsorgsync sync_stsorgsync_users getting list of users from stsorgsync
    INFO 2019-05-03 12:02:45,484 mox_stsorgsync sync_stsorgsync_users getting list of users from os2mo
    INFO 2019-05-03 12:02:47,362 mox_stsorgsync sync_stsorgsync_users deleting os2mo-deleted users in stsorgsync
    INFO 2019-05-03 12:02:47,362 mox_stsorgsync sync_stsorgsync_users upserting stsorgsync users
    INFO 2019-05-03 12:02:48,024 mox_stsorgsync upsert user a1bc5918-a19b-4798-8788-ca43a97cd707
    ...
    INFO 2019-05-03 12:05:50,208 mox_stsorgsync upsert user f28b1d87-12b7-4555-a667-614a773ccc0f
    INFO 2019-05-03 12:05:50,284 mox_stsorgsync sync_stsorgsync_users done
    INFO 2019-05-03 12:05:50,284 mox_stsorgsync mox_stsorgsync done


