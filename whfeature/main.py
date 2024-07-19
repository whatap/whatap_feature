import npyscreen
from forms.login import LoginForm
from forms.feature import MainForm, StatusSelectForm

class MyApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", MainForm)
        self.addForm("LOGIN", LoginForm)
        self.addForm('STATUSSELECT', StatusSelectForm)
        self.setNextForm("LOGIN")

if __name__ == "__main__":
    app = MyApp()
    app.run()
