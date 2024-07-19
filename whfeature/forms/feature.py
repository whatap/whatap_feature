import npyscreen
import features
import logging
import helper.whatap_helper as whatap_helper

import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Create a file handler for the log file
file_handler = logging.FileHandler('.debug.log')
file_handler.setLevel(logging.DEBUG)

# Create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)


def getLocalFeatureAll():
    # fl = { f['textKey']: f  for f in whatap_helper.getFeatureAll() }

    for (tk, name, desc) in features.listAll():
        yield (tk, name, desc, 'N/A')  

def getFeatureAll():
    
    fl = { f['textKey']: f  for f in whatap_helper.getFeatureAll() }

    feature_lookup = {}
    for (tk, name, desc) in features.listAll():
        feature_lookup[tk]= (tk, name, desc, 'offline')
    for f in whatap_helper.getFeatureAll():
        tk = f['textKey']
        name = f['name']
        desc = f['description']
        status = f['status']
        feature_lookup[tk] = (tk, name, desc, status)
    return list(feature_lookup.values())

def fetchFeatureStatus(feature):
    fl = { f['textKey']: f  for f in whatap_helper.getFeatureAll() }

    (tk, name,description, status) = feature
    if tk in fl:
        return (tk, name,description, fl[tk]['status'])
    
    return feature 

def updateFeatureStatus(tk, status):
    whatap_helper.updateFeatureStatus(tk, status)

def uploadFeature(tk):
    feature = features.getByTextKey(tk)
    if not feature:
        raise Exception(f"feature {tk} not found")
    whatap_helper.uploadFeature(tk, feature)

class FeatureList(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(FeatureList, self).__init__(*args, **keywords)
        self.add_handlers({
            "a": self.when_action
        })

    def display_value(self, vl):
        return f"{vl[0]}"

    def actionHighlighted(self, act_on_this, key_press):
        self.parent.display_feature_properties(act_on_this)

    def when_action(self, *args, **keywords):
        npyscreen.notify_confirm("Performing action on selected feature", title="Action")


class FeatureProperties(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(FeatureProperties, self).__init__(*args, **keywords)
        self.add_handlers({
            "u": self.upload_feature
        })
        self.selected_feature = None

    def display_value(self, vl):
        return vl

    def update_properties(self, feature):
        self.selected_feature = feature
        self.values = [
            f"Name: {feature[1]}",
            f"TextKey: {feature[0]}",
            f"Description: {feature[2]}",
            f"Status: {feature[3]}",
            "Upload"
        ]
        self.display()

    def actionHighlighted(self, act_on_this, key_press):
        if act_on_this == "Upload":
            self.upload_feature()
        elif act_on_this.startswith("Status: "):
            #want to select status and update feature
            self.changeStatus()

    def changeStatus(self):
        self.parent.parentApp.getForm('STATUSSELECT').parent_feature = self
        self.parent.parentApp.switchForm('STATUSSELECT')

    def upload_feature(self, *args, **keywords):
        if self.selected_feature:
            feature_name = self.selected_feature[1]
            feature_tk = self.selected_feature[0]
            try:
                uploadFeature(feature_tk)
                npyscreen.notify_confirm(f"Feature {feature_name} uploaded successfully!", title="Upload Feature")
                self.values[3] = f"Status: {feature_name} uploaded"
                self.display()
            except Exception as e:
                import traceback
                stack_trace = traceback.format_exc()
                logger.debug(stack_trace)
                npyscreen.notify_confirm(f"Feature upload error {e}", title="Feature Upload Error")
            
class StatusSelectForm(npyscreen.ActionPopup):
    def create(self):
        self.name = "Select Status"
        self.status_options = self.add(npyscreen.TitleSelectOne, max_height=4, value=[0,], name="Status",
                                       values=["open", "beta", "preview", "closed"], scroll_exit=True)
        self.parent_feature = None

    def on_ok(self):
        if self.parent_feature:
            selected_status = self.status_options.get_selected_objects()[0]
            tk = self.parent_feature.selected_feature[0]
            try:
                updateFeatureStatus(tk, selected_status)
                self.parent_feature.values[3] = f"Status: {selected_status}"
                self.parent_feature.display()
                npyscreen.notify_confirm(f"Status updated to {selected_status}", title="Status Update")
            except Exception as e:
                npyscreen.notify_confirm(f"Status update error {e}", title="Status Update Error")
                
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()


class MainForm(npyscreen.Form):
    def create(self):
        self.name = "Feature Management"
        # Split layout
        split_ratio = 0.3
        max_cols = self.columns
        left_pane_width = int(max_cols * split_ratio)
        
        # Left pane - Feature List
        self.feature_list = self.add(FeatureList, name="Features", max_width=left_pane_width, relx=2, rely=2, max_height=self.lines-6)
        
        # Right pane - Feature Properties
        self.feature_properties = self.add(FeatureProperties, name="Feature Properties", relx=left_pane_width + 4, rely=2, max_height=self.lines-6)
        
        # Load features
        # self.load_features()

    def beforeEditing(self):
        self.load_features()

    def load_features(self):
        self.features = getFeatureAll()
        feature_names = [(f[0], f[1], f[2], f[3]) for f in self.features]
        self.feature_list.values = feature_names
        self.feature_list.display()

    def display_feature_properties(self, feature):
        feature = fetchFeatureStatus(feature)
        self.feature_properties.update_properties(feature)



# class MainForm(npyscreen.ActionForm):
#     def create(self):
#         self.name = "Main Page"
#         self.add(npyscreen.FixedText, value="Feature List", editable=False)
#         self.table_with_header = self.add(FeatureTableWithHeader, name="Feature List", max_height=15)
#         ftvalues = []
#         for textkey, name, description in features.listAll():
#             ftvalues.append((textkey, name, description))
#         self.table_with_header.entry_widget.values = ftvalues
#         self.upload_all_button = self.add(npyscreen.ButtonPress, name="Upload All")
#         self.upload_all_button.whenPressed = self.upload_all

#     def upload_all(self):
#         npyscreen.notify_confirm("Uploading all features", title="Upload All")

#     def on_ok(self):
#         self.parentApp.setNextForm(None)

#     def on_cancel(self):
#         self.parentApp.setNextForm(None)
