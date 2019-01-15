# Moscow_Date_Generator_Bot
Telegram Bot (RU). Asks for starting point and preferences for generating several places for visiting during your rendezvous.

Python, Git, Heroku, Yandex Map API, pipenv, pylint, Jupyter Notebook and libs such as telebot, pandas, sqlite3, requests, re, random.

Programm has 3 layers:
  1. User interactor.
  2. Date Generator. Takes input from the upper level, queries inner layer for places, postprocesses response and passes it to the user interactor.
  3. The inner layer consists of two parts: DB and API interactors.

There are several obvious potential updates:
  1. Bot's appearance can be more attractive with pictures, diverse texts, and jokes (there is one though, try to choose places randomly)
  2. Programm takes info from two sources (DB and API). I suppose Yandex maps updates faster than data.mos.ru, but considering the main purpose of creating of this bot is to show some basic programming skills, I decided to use both.
  3. Programm has OOP-styled parts, it gives some space for scaling. 

But it makes sense to transform code a bit for further scaling.
