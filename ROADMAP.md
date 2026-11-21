# TMU CS Discord bot: roadmap

The goal: a Python bot that checks TMU's website for new key dates, events
and news, and posts anything new in the TMU CS server's announcement channel.
Students can also ask it things, such as `/dates` for the next deadlines.

You write the code; I explain each idea and check what you write.
Tick a box when a step is done.

## What I found on TMU's site (2026-11-21)

- TMU has **no RSS feeds**, so the bot has to read the web pages themselves ("scraping").
- The `/news-events/` hub page has its stories and upcoming events in the plain HTML, which makes it the easiest place to start.
- The full lists on `/news-events/news/`, `/news-events/events/` and `/cs/news-events/` are loaded by JavaScript after the page opens. Your browser's DevTools (Network tab) will show where that data comes from. You'll look into that in Step 6.
- The old key-dates address (`/registrar/dates/`) no longer works. Finding where key dates live now is part of Step 6.
- TMU's `robots.txt` (the file that tells bots what they may read) does not block any of these pages. We'll still be polite: check every 30-60 minutes, not every few seconds.
- The CS department's seminar calendar is a public Google Calendar. That could be a later extra.

## Part 0: before any code

- [ ] **Step 0 - Get permission and a test server.**
  - Ask the TMU CS server's admins if they're OK with the bot, and which channel it should post in.
  - Make your own private Discord server to test in, so mistakes don't land in front of everyone.
  - You learn: real projects begin with the people who'll use them.

## Part 1: post to Discord (no bot needed yet)

- [ ] **Step 1 - Setup.** Project folder, virtual environment, `git`, a `.env` file for secrets, and a `.gitignore` that keeps `.env` out of git.
- [ ] **Step 2 - Send your first message with a webhook.** A webhook is a secret URL that posts into one channel. You make it in channel settings, then send it a message using `requests`, the same tool you used for NASA.
  - You learn: sending data to an API (POST), as well as reading from one (GET).
  - At the end: running `py main.py` makes "Hello from Python" show up in your test channel.
- [ ] **Step 3 - Make it look good.** Send an embed: a card with a title, link, date and TMU blue colour.
  - You learn: building nested dictionaries for an API (the reverse of digging into NASA's).

## Part 2: read TMU's website

- [ ] **Step 4 - Download a page and find the parts you need.** Fetch `/news-events/` and use BeautifulSoup to pull out each story's title, link and summary, and each event's title, date and place.
  - You learn: what HTML is, inspecting a page in the browser, and `BeautifulSoup`.
  - At the end: a list of dictionaries, one per item, printed in the terminal.
- [ ] **Step 5 - Remember what's already posted.** Save the link of every item you've posted, and only post items whose link is new.
  - You learn: saving data between runs. Start with a JSON file, then move to `sqlite3`, the small database built into Python.
  - At the end: running it twice posts the new items once, and nothing the second time.
- [ ] **Step 6 - More sources.** Use DevTools to find where the news, events and CS-news lists get their data, find the current key-dates page, and add each as its own source.
  - You learn: how websites load data behind the scenes, and writing one function per source that all return the same shape of data.

## Part 3: make it a real bot

- [ ] **Step 7 - Run it on a timer.** Check every 30-60 minutes, and don't crash if TMU's site is down or changes.
  - You learn: loops with `time.sleep`, `try`/`except`, and logging.
- [ ] **Step 8 - Switch to a real bot account.** Create an application in the Discord Developer Portal and connect with `discord.py`. Its scheduled tasks take over from the timer in Step 7.
  - You learn: `async`/`await`, which is how Python does several things at once, and bot tokens and permissions.
- [ ] **Step 9 - Slash commands.** `/dates` shows the next few key dates, `/events` shows this week's events, and `/latest` shows the newest news.
  - You learn: responding to users, and reading from your own database.

## Part 4: go live

- [ ] **Step 10 - Keep it running 24/7.** Your PC turns off, so the bot needs a home: a free cloud server, a Raspberry Pi, or a cheap paid host. We'll compare them when you get here.
- [ ] **Step 11 - Launch.** Add the bot to the TMU CS server with only the permissions it needs, post in the agreed channel, and watch the first day closely.
- [ ] **Step 12 - Publish.** README, push to GitHub (with no secrets in it), and add it to your portfolio.

## Rules for the whole project

- Never put the webhook URL or bot token in code or on GitHub. They go in `.env` only. Anyone who has them can post as your bot.
- Always test in your own server first.
- If TMU changes its site, the scraper will break. That's normal. Step 7's error handling makes sure it fails quietly instead of spamming the channel.
