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


The configuration file has the following settings

    [settings]

    ; log level set this to a numeric representation of a log level - 10 is debug
    MOX_LOG_LEVEL = 10 

    ; log file - set this to blank to have log in stderr, otherwise this must be a file name 
    MOX_LOG_FILE =

    ; os2mo-service url - this is the full url to os2mo-service - it must end in '/service'
    OS2MO_SERVICE_URL = 

    ; os2mo saml token - if You are running an authenticvated OS2MO, You must use this access token
    OS2MO_SAML_TOKEN =

    ; os2mo org uuid - leqave it blank to have this mox figure it out by itselv 
    OS2MO_ORG_UUID = 
    
    ; os2mo ca bundle - 'true' means use the built in ca-bundle, 'false' means dont use any
    ; otherwise it is interpreted as a filename where the ca certs are
    OS2MO_CA_BUNDLE = true

    ; stsorgsync api url - this is the url to the stsorgsync instance - it will typically end with '/api/v1_1' or similar 
    STSORGSYNC_API_URL = http://some-stsorgsync-url/api/v1_1

    ; stsorgsync ca bundle - 'true' means use the built in ca-bundle, 'false' means dont use any
    ; otherwise it is interpreted as a filename where the ca certs are
    STSORGSYNC_CA_BUNDLE = true


