# Feature Project - Server Monitoring Add-on

The Feature Project is a package of add-ons for server monitoring that can be registered and modified through an API on the Suzi server. This management program allows users to log in, view feature lists, and upload features to the collection server.

## Usage Instructions

1. **Download the Release Executable:**
   Download the executable file from the release section of this repository.

2. **Run the Executable:**
   Execute the downloaded file to start the management program.

3. **Login:**
   The first screen you will see is the login page. Enter your username, password, and the Whatap URL to log in.
   ![image](https://github.com/user-attachments/assets/97f7120a-e705-423b-b155-6c0a34fc3fbd)

4. **View Feature List:**
   After logging in, you will be presented with the feature management screen where you can see a list of available features.
   ![image](https://github.com/user-attachments/assets/22ff00ab-1c92-44f4-821e-460afbce911c)

5. **Upload a Feature:**
   Select the feature you wish to upload and press the 'Upload' button.
   ![image](https://github.com/user-attachments/assets/3df488a6-2352-4f93-9de1-9e21e7ff5911)

6. **Upload Completion:**
   A confirmation message will appear once the feature is successfully uploaded.

   ![image](https://github.com/user-attachments/assets/c877a56c-ebef-44d9-b3f4-1f6f51e1d8bf)

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
