import time

import mailtrap as mt


class MYMAIL:
    def __init__(self, token, from_email, to_email):
        self.token = token
        self.client = self.set_client(token=token)
        self.from_email = from_email
        self.to_email = to_email

    def get_client(self):
        return self.client

    def set_client(self, token):
        self.client = mt.MailtrapClient(token=token)
        return self.client

    def send_email(self, subject, text):
        mail = mt.Mail(
            sender=mt.Address(email=self.from_email, name="Adam Bot"),
            to=[mt.Address(email=self.to_email)],
            subject=subject,
            text=text,
            category="A",
        )
        return self.client.send(mail)


if __name__ == "__main__":
    token = "1cce7d6061aa19710124f0e2ca013fd2"
    from_email = "hello@demomailtrap.co"
    to_email = "boenchen0839@gmail.com"
    subject = f'测试 {time.strftime("%Y/%m/%d %H:%M:%S")}'
    text = f'test'

    email = MYMAIL(token, from_email, to_email)
    email.send_email(subject, text)
