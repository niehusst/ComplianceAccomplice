# Compliance Accomplice
An email system middleware for detecting and archiving potential SEC compliance issues in a self-hosted email server using Natural Language Processing (NLP).

## How does it work?
Compliance Accomplice parses a user's email text after they click the send button to search for possibly non-compliant
words and phrases. If it finds words that are in a collection of unprofessional speech or if it finds phrases or
sentences that the Google Cloud NLP AI deems as imperative language, the message is intercepted. Compliance
Accomplice then sends a response email back to the sender, suggesting they change the portions of the email
that were flagged as profane or non-compliant.
If the user still desires to send the message unaltered, they can reply with anything to Compliance Accomplice email
and the original email will be sent unaltered. To change the email, the user just writes a new one.
Any attached files will be sent along either way. There is currently no support for scanning them for compliance.

## How does it look on the receiving side?
Since all sent emails go through Compliance Accomplice so they can be analyzed and stored in the server inbox, the emails will come from

`compliance.accomplice+emailuser+domain+extension@gmail.com`.

However, for ease of use, the reply field is automatically filled in
to be the email address the user sent the original email from. This simulates the behavior that would be found on a self-hosted server, where the emails could be intercepted without this url redirection.

## How can I use this?
Integrating this system into your company only requires changes in your
email system configuration. To enable Compliance Accomplice to see your email, you
must send emails through the filter installed on your own server (using incoming/outgoing ports to block the message from sending before filter) and the system would use normal addresses.

### Authors
 * **Bogdan Abaev** - [abaevbog](https://github.com/abaevbog)
 * **Liam Niehus-Staab** - [niehusst](https://github.com/niehusst)
 * **Philip Kiely** - [philipkiely](https://github.com/philipkiely)

### Sources/Acknowledgements
 * [Google Cloud NLP](https://cloud.google.com/natural-language/) for sentiment assessment of text.
 * [LDNOOBW](https://github.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words) for dataset of profane words.
 * [Tailor Brands](https://www.tailorbrands.com/) for the logo.
