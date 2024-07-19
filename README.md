# Feature Project - Server Monitoring Add-on

The Feature Project is a package of add-ons for server monitoring that can be registered and modified through an API on the Suzi server. This management program allows users to log in, view feature lists, and upload features to the collection server.

## Usage Instructions

1. **Download the Release Executable:**
   Download the executable file from the release section of this repository.

2. **Run the Executable:**
   Execute the downloaded file to start the management program.

3. **Login:**
   The first screen you will see is the login page. Enter your username, password, and the Whatap URL to log in.

   ![Login Page](path/to/your/image1.png)

4. **View Feature List:**
   After logging in, you will be presented with the feature management screen where you can see a list of available features.

   ![Feature Management](path/to/your/image2.png)

5. **Upload a Feature:**
   Select the feature you wish to upload and press the 'Upload' button.

   ![Upload Feature](path/to/your/image3.png)

6. **Upload Completion:**
   A confirmation message will appear once the feature is successfully uploaded.

   ![Upload Successful](path/to/your/image4.png)

## Example Workflow

1. **Login to the System:**
   ```plaintext
   Username: sa@whatap.io
   Password: **********
   Whatap URL: https://dev.whatap.io

   Log Output:
   - begin login...
   - connecting...
   - login success!
2. **View and Select Feature:**

```plaintext
Feature Management
-------------------
KAFKA
VCENTER_DEV_0625
VCENTER_DEV_ONE

Name: KAFKA
TextKey: KAFKA
Description: KAFKA BETA RC 0604
Status: beta
Upload the Selected Feature:

```plaintext
Status: KAFKA uploaded
Upload Confirmation:

```plaintext
Feature Management
-------------------
Feature KAFKA uploaded successfully!
