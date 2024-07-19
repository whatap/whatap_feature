import npyscreen
import time
import threading
import helper.whatap_helper as whatap_helper

class LoginForm(npyscreen.ActionForm):
    def create(self):
        self.name = "Login Page"
        username, whatap_url = whatap_helper.load()
        self.username = self.add(npyscreen.TitleText, name="Username:", value=username)
        self.password = self.add(npyscreen.TitlePassword, name="Password:")
        self.whatap_url = self.add(npyscreen.TitleText, name="Whatap URL:", value=whatap_url)
        self.log_output = self.add(npyscreen.BoxTitle, name="Log Output:", max_height=10, editable=False)

    def on_ok(self):
        # 로그인 시도 로그 출력
        self.log_message("begin login...")
        
        # 비동기 로그인 시뮬레이션 시작
        login_thread = threading.Thread(target=self.login_process)
        login_thread.start()
    
    def log_message(self, message):
        current_log = self.log_output.values
        current_log.append(message)
        self.log_output.values = current_log
        self.log_output.display()

    def login_process(self):
        # 첫 번째 로그 단계
        time.sleep(1)
        self.log_message("connecting...")
        
        try:
            # 로그인 처리
            if whatap_helper.login(self.username.value, self.password.value, self.whatap_url.value):
                # 로그인 성공 로그 출력
                self.log_message("login success!")
                self.parentApp.setNextForm("MAIN")
                # 메인 폼으로 전환
                self.parentApp.switchForm("MAIN")
        except Exception as e:
            # 로그인 실패 로그 출력
            self.log_message(f"login fail: {e}")
            
        
    def on_cancel(self):
        self.parentApp.setNextForm(None)
