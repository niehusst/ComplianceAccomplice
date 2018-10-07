# Compliance Accomplice
An email add-on for detecting and archiving SEC compliance in a server using Natural Language Processing (NLP).

## How does it work?
Compliance Accomplice parses a users email text after they click the send button to search for possibly non-compliant
words and phrases. If it finds words that are in a collection of unbuisness-like words or if it finds phrases or
sentences that the Google Cloud NLP AI deems as imperative language, the message is intercepted. Compliance
Accomplice then sends a response email back to the sender, suggesting they change the portions of the email
that was flagged as profane or non-compliant.
If the user still desires to send the message unaltered, they can reply with anything to Compliance Accomplice email
and the original email will be sent unaltered. To change the email, the user must write a new one.
Any attached files will be sent along either way. There is currently no support for scanning them from compliance.

## How does it look on the receiving side?
Since all sent emails go through Compliance Accomplice so they can be analyzed and stored in the server inbox, the emails will come from

`compliance.accomplice+emailuser+domain+extension@gmail.com`.
However, for ease of use, the reply field is automatically filled in
to be the email address the user sent the original email from.

## How can I use this?
Integrating this system into your company only requires changes in your
address book. To enable Compliance Accomplice to see your email, you
must send emails through the Compliance Accomplice gmail account with
the true intended recipient email included with plusses. For example;

`Original intended recipient: recipient3@gmail.com`

`New target address: compliance.accomplice+recipient3+gmail+com@gmail.com`

To change your address book to this format, you could use the program
.......
???

### Authors
 * **Bogdan Abaev** - [abaevbog](https://github.com/abaevbog)
 * **Liam Niehus-Staab** - [niehusst](https://github.com/niehusst)
 * **Philip Kiely** - [philipkiely](https://github.com/philipkiely)

### Sources/Acknowledgements
 * [Google Cloud NLP](https://cloud.google.com/natural-language/) for sentiment assesment of text.
 * [LDNOOBW](https://github.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words) for dataset of profane words.
 * [Tailor Brands](https://www.tailorbrands.com/) for the logo.
