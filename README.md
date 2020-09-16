# TvinnaMonitor
A script which monitors the Tvinna (https://www.tvinna.is/) website for new job advertisements and notifies with an email when there are new entries.

## Functionality
The script runs continuously and periodically checks Tvinna for new job advertisement entries. When new entries are found since last check, an email is sent with notification about these new entries, including a list of the entries where each entry contains the company's name, the position's name and a URL.

currentNewJobs.txt is used to keep track of which job advertisements were present on Tvinna when it was last updated. This list of advertisements is used to compare to new data fetched from Tvinna. If the newest data from Tvinna has an advertisement(s) which is not present on this list, then a new job advertisement has been posted on Tvinna and an email is sent with that information.

## Logs
Everytime Tvinna is checked for new advertisements, a log is made in logs.txt. Each log entry indicates whether new advertisements were found or not. If new job advertisements are found, they are included in the log.

## NOTE
To try out the email functionality, please contact me for Mailgun API authorization information.
