# TMU CS Discord bot: roadmap

The goal: a Python bot that knows TMU's key dates (enrolment, term start and
end, exams, fees, holidays) and keeps the TMU CS server up to date. It posts
a weekly "coming up" list, reminds everyone the day before big deadlines,
announces when TMU adds or changes a date, and answers questions such as
`/dates` and `/courses`.

You write the code; I explain each idea and check what you write.
Tick a box when a step is done.

## Where the data comes from (checked 2026-11-21)

- **Key dates:** TMU's Significant Dates page,
  `https://www.torontomu.ca/calendar/2026-2027/dates/`. It's one HTML table
  with about 310 rows. Each row has: start date (`YYYY-MM-DD`), end date
  (sometimes `TBD`), category, subject and description. The first row is the
  column names.
- **Categories in that table:** Enrolment and Refund Dates (the biggest, 143
  rows), Session Start and End Dates, Exam Dates, Fees and Tuition Dates,
  Holidays and Observances, Grades/Standings/Appeals, Graduation and
  Convocation, Chang School dates, Admissions Deadlines, Transfer Credit
  Deadlines.
- **CS courses:** the CS program page,
  `/cs/current-undergraduate-students/curriculum-courses/computer-science-program/`,
  lists the required courses for each semester in tables.
- TMU has no RSS feeds, so the bot reads the pages themselves ("scraping").
  TMU's `robots.txt` allows these pages. We stay polite: a few checks a day
  are plenty, because key dates change rarely.
- **Watch out:** the address has the school year in it (`2026-2027`). When
  TMU publishes the 2027-2028 dates, the bot has to switch to the new address.

## Part 0: before any code

- [x] **Step 0 - Get permission and a test server.**
  - Ask the TMU CS server's admins if they're OK with the bot, and which channel it should post in.
  - Make your own private Discord server to test in, so mistakes don't land in front of everyone.

## Part 1: post to Discord

- [x] **Step 1 - Setup.** Project folder, virtual environment, `git`, `.env`, `.gitignore`, `requirements.txt`.
- [x] **Step 2 - First webhook message.** POST to a Discord webhook with `requests`.
- [x] **Step 3 - Embeds.** `send_discord_message()` sends a TMU-blue card with a title, description and link.

## Part 2: read the key dates

- [ ] **Step 4 - Read the table.** `get_key_dates()` downloads the Significant Dates page and turns every row into a dictionary: `start`, `end`, `category`, `subject`, `description`.
  - You learn: HTML tables, BeautifulSoup, and list comprehensions.
  - At the end: about 310 dates in a list, printed in the terminal.
- [ ] **Step 5 - Real dates and filtering.** Turn the date text into real dates. Keep the rows that matter to CS students and drop the rest (for example Engineering-only, Architectural Science and Chang School rows).
  - You learn: the `datetime` module, comparing dates, handling odd values like `TBD`, and writing filter functions.
  - At the end: `dates_between(start, end)` returns, for example, every CS-relevant date in the next 7 days.
- [ ] **Step 6 - Weekly digest.** One embed that lists the coming week's dates in a clean, readable way, grouped or sorted by date.
  - You learn: building longer messages, Discord's size limits, and formatting dates nicely.
  - At the end: running the script posts "This week at TMU" to your test channel.

## Part 3: remember and react

- [ ] **Step 7 - Remember what the bot knows.** Save a copy of the dates after each check. Next time, compare: which dates are new, and which have changed?
  - You learn: saving data between runs. Start with a JSON file, then move to `sqlite3`, the small database built into Python.
  - At the end: "TMU added/changed a date" announcements, and day-before reminders that never post twice.
- [ ] **Step 8 - Run on a schedule.** Check TMU a few times a day, post the digest every Monday morning, and send reminders the day before. Don't crash if TMU's site is down or changes.
  - You learn: scheduling, `try`/`except`, and logging.

## Part 4: make it a real bot

- [ ] **Step 9 - Switch to a real bot account.** Create an application in the Discord Developer Portal and connect with `discord.py`. Its scheduled tasks take over from Step 8.
  - You learn: `async`/`await`, bot tokens and permissions.
- [ ] **Step 10 - Slash commands.**
  - `/dates`: the next few key dates.
  - `/deadline <word>`: search the dates, e.g. `/deadline drop` or `/deadline winter`.
  - `/courses <semester>`: the CS courses for that semester, read from the CS program page.
  - You learn: responding to users, command options, and reading from your own database.

## Part 5: go live

- [ ] **Step 11 - Keep it running 24/7.** Your PC turns off, so the bot needs a home: a free cloud server, a Raspberry Pi, or a cheap paid host. We'll compare them when you get here.
- [ ] **Step 12 - Launch.** Add the bot to the TMU CS server with only the permissions it needs, post in the agreed channel, and watch the first week closely.
- [ ] **Step 13 - Publish.** README, push to GitHub (with no secrets in it), and add it to your portfolio.

## Ideas for later

- Course enrolment tips from TMU's Course Enrolment page (`/current-students/course-enrolment/`).
- CS department seminars from its public Google Calendar.
- Let each student choose which reminders they get, using Discord roles.

## Rules for the whole project

- Never put the webhook URL or bot token in code or on GitHub. They go in `.env` only. Anyone who has them can post as your bot.
- Always test in your own server first.
- If TMU changes its site, the scraper will break. That's normal. Step 8's error handling makes sure it fails quietly instead of spamming the channel.
