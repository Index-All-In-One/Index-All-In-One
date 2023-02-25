# Importing libraries
import imaplib, email

user = 'a1415217miss@gmail.com'
# password = ''
imap_url = 'imap.gmail.com'

# Function to get email content part i.e its body part
def get_body(msg):
	if msg.is_multipart():
		return get_body(msg.get_payload(0))
	else:
		return msg.get_payload(None, True)

# Function to search for a key value pair
def search(key, value, imap_server):
	result, data = imap_server.search(None, key, '"{}"'.format(value))
	return data

# Function to get the list of emails under this label
def get_emails(message_numbers):
	msgs = [] # all the email data are pushed inside an array
	for num in message_numbers:
		# RFC822: feachable message
		typ, data = imap.fetch(num, '(RFC822)')
		msgs.append(data)

	return msgs

if __name__ == "__main__":
	# this is done to make SSL connection with GMAIL
	imap = imaplib.IMAP4_SSL(imap_url)
	# logging the user in
	imap.login(user, password)
	# calling function to check for email under this label
	imap.select('Inbox')

	success, message_numbers = imap.search(None, 'ALL')
	message_numbers = message_numbers[0].split()
	print(message_numbers)

	msgs = get_emails(message_numbers)
	# print(msgs[0][0][1])

	message = email.message_from_bytes(msgs[4][0][1])

	print("Message number 0")
	print(f"From: {message.get('From')}")
	print(f"to: {message.get('To')}")
	print(f"BCC: {message.get('BCC')}")
	print(f"Date: {message.get('Date')}")
	print(f"Subject: {message.get('Subject')}")

	print(f"Content:")
	for part in message.walk():
		if part.get_content_type() == "text/plain":
			print(part.as_string())

	imap.close()