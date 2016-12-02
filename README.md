# birthdaynotifier

Application sends emails from your gmail account, using google smtp server. If you use 2 factor authentification, make an [application password](https://security.google.com/settings/security/apppasswords?pli=1)
No more than 99 emails per day are alowed.

example of a valid json file:

```
[
  {
    "name": "juozas",
    "email": "test@test.com",
    "birthdate": "1990-03-19"
  },
  {
    "name": "test",
    "email": "test@test.lt",
    "birthdate": "02-17"
  },
  {
    "name": "random",
    "email": "random@random.lt",
    "birthdate": "12-03"
  }
]

```