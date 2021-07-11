# Mass Personalised Emailing with Firebase 

A simple Python script connected to Firebase for sending mass personalised confirmation email. The Python script reads from a csv file with the receivers' details and a text file with the email content written in HTML. 

## Repository Files

<b>Mass Mailer Script</b>: The Python script is in the `massMailer.py` file. <br>
<b>Email content</b>: The email content written in HTML is found in the `mailContent.txt` file. <br>
<b>Receiver Details</b>: The receivers' details are in the `receiverDetails.csv` file. <br>

## How to use

### Step 1: Set up the configurations for your Firebase.

```
config = { 
  "apiKey": "your-firebase-api-key",
  "authDomain": "your-firebase-auth-domain",
  "databaseURL": "your-firebase-database-url",
  "storageBucket": "your-firebase-storage-bucket",
}
```

### Step 2: Install Pyrebase and run the script

```
pip install pyrebase
python massMailer.py
```

### Step 3: Log in to your Gmail account

The console will prompt you for your login credentials. Enter the credentials of the Gmail account you want to send your emails from.

```
Login
Enter your gmail: <your email address>
Enter your password: <your password>
```

## How it works 

### Connect to Firebase

```
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
```

### Read the HTML email content from txt file

```
def sendMail():
    mail_body = read_template('mailContent.txt')
```
### Login to the sender's email account via SMTP 

Enter your own login credentials to login to your gmail via SMTP.
```
print("Login")
    email = input("Enter your gmail: ")
    password = input("Enter your password: ")

    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(email, password)
 ```
 
 ### Read the csv file to get the receivers' email addresses
 
 ```
 with open("receiverDetails.csv", "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)
        for row in csv_reader:
            user_email = row[10].strip()
 ```
 
 ### Generate login password on Firebase for each receiver 
 
 ```
 def generatePassword():
    length = 11
    upper = string.ascii_uppercase
    lower = string.ascii_lowercase
    num = string.digits

    all = lower + upper + num
    temp = random.sample(all, length)

    password = "".join(temp)
    return password
  ```
  
 ### Create user for each receiver on Firebase based on their email address and randomly generated password
  
  `createUser(user_email, user_password)`
  
 ### Add their name, email address and password into email content to personalise the email
 
 `message = mail_body.format(PERSON=row[7].strip().upper(), USERNAME=user_email, PASSWORD=user_password)`

### Write the subject line

```
 msg['From'] = email
            msg['To'] = row[10]
            msg['Subject'] = '[Confirmation] Test Email Send'

            msg.attach(MIMEText(message, 'html'))
```

### Send the email!

`s.send_message(msg)`
