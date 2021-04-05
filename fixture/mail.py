import poplib
import email
import time


class MailHelper:
    def __init__(self, app):
        self.app = app

    def get_mail(self, username, password, subject):
        # делаем 5 попыток (по 3 сек ожидания) на получение письма
        for i in range(5):
            pop = poplib.POP3(self.app.config['james']['host'])
            pop.user(username)
            pop.pass_(password)
            # кортеж, где 0 индекс отвечает за количество писем
            num = pop.stat()[0]
            if num > 0:
                for n in range(num):
                    # преобразование тела письма (индекс 1) в текст
                    msglines = pop.retr(n + 1)[1]
                    msgtext = "\n".join(map(lambda x: x.decode('utf-8'), msglines))
                    msg = email.message_from_string(msgtext)
                    # роверяем что письмо с искомой темой
                    if msg.get("Subject") == subject:
                        pop.dele(n + 1)
                        pop.quit()
                        return msg.get_payload()
            pop.close()
            time.sleep(3)
        return None
