# TMU CS Discord Bot

A Python bot that keeps students in the TMU Computer Science Discord server on
top of key academic dates. It reads Toronto Metropolitan University's
[Significant Dates](https://www.torontomu.ca/calendar/2026-2027/dates/) page
and posts a reminder to Discord **3 days before** each date starts, and again
3 days before it ends.

> Unofficial student project. Not affiliated with Toronto Metropolitan
> University. Always check TMU's official page for the final word on dates.

## What it does

- **Reads TMU's key dates.** Downloads the Significant Dates table (about 310
  dates: enrolment, waitlists, term start and end, exams, fees, holidays, grades)
  and turns each row into a Python dictionary.
- **Keeps only what matters to CS students.** Skips Engineering-only and Chang
  School dates, but keeps rows that apply to everyone (for example "classes
  other than Engineering").
- **Posts reminders 3 days ahead.** Each reminder is a Discord embed with the
  date's name, TMU's description, its start and end dates, and a link to the
  official page.
- **Never posts the same reminder twice.** Every posted reminder is recorded
  in `sent_reminders.json`. If the bot misses a day, it still catches up on
  anything coming up in the next 3 days.

## Example

> **Ends Soon: Fall Term Undergraduate Examination Period**
> Examination Period includes Saturdays and Sundays.
>
> Start: Wednesday, December 09
> End: Sunday, December 20

## Built with

- Python 3.14
- [requests](https://pypi.org/project/requests/): downloads the page and sends messages to Discord
- [Beautiful Soup](https://pypi.org/project/beautifulsoup4/): reads the HTML table
- [python-dotenv](https://pypi.org/project/python-dotenv/): loads the webhook URL from `.env`
- Discord webhooks: post messages to a channel

## Run it yourself

1. Clone the repo and open the folder.
2. Create and activate a virtual environment:
   ```
   py -m venv venv
   venv\Scripts\activate
   ```
3. Install the packages:
   ```
   pip install -r requirements.txt
   ```
4. In your Discord server, open a channel's settings, then **Integrations → Webhooks → New Webhook**, and copy its URL.
5. Create a file called `.env` in the project folder:
   ```
   DISCORD_WEBHOOK_URL=your-webhook-url-here
   ```
   Keep this file private. Anyone with the URL can post in your channel.
6. Run the bot:
   ```
   py bot.py
   ```
   It prints how many reminders were due and how many it sent, for example
   `2026-11-28: 2 due, 2 sent`.

## Plans

- Run automatically every morning with GitHub Actions
- Detect when TMU adds or changes a date
- Become a full Discord bot with slash commands such as `/dates`, `/deadline` and `/courses`

## Note

The data comes from TMU's public website. The page's address includes the
school year (`2026-2027`), so it needs updating when TMU publishes the next
year's dates.
