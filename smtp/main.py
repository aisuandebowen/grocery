import mailtrap as mt


def mailtrip_demo():
    token = "1cce7d6061aa19710124f0e2ca013fd2"
    mail = mt.Mail(
        sender=mt.Address(email="hello@demomailtrap.co", name="Adam Bot"),
        to=[mt.Address(email="boenchen0839@gmail.com")],
        subject="你吃饭了么",
        text="1111111111111111",
        category="222",
    )

    client = mt.MailtrapClient(token=token)
    response = client.send(mail)

    print(response)


def run():
    mailtrip_demo()


if __name__ == "__main__":
    run()
