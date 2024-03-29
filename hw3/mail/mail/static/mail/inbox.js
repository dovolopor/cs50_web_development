var currentMailBox = "";
var shownMailID = 0;
var shownMail;

document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').onsubmit = sendMail;
  document.querySelector('#archive-btn').onclick = archiveShownMail;
  document.querySelector('#reply-btn').onclick = replyShownMail;

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#compose-errmsg').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view-title').innerHTML = mailbox.charAt(0).toUpperCase() + mailbox.slice(1);

  currentMailBox = mailbox;
  document.querySelector('#emails-show').style.display = 'none';
  fetch('/emails/' + mailbox)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      console.log(emails);
      // ... do something else with emails ...

      fillEmailsView(emails)
  });

  let archiveBtn = document.querySelector('#archive-btn');
  switch (mailbox) {
    case "inbox":
      archiveBtn.style.display = "inline-block"
      archiveBtn.innerHTML = "Archive"
      
      break;

    case "archive":
      archiveBtn.style.display = "inline-block"
      archiveBtn.innerHTML = "Unarchive"
      break;
  
    default:
      archiveBtn.style.display = "none"
      break;
  }
}

function sendMail()
{
  // validate fields
  if(document.forms["compose-form"]["compose-recipients"].value === "")
  {
    alertnewMailForm("Message recipent cannot be empty")
    return false
  }

  // send the email
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: document.forms["compose-form"]["compose-recipients"].value,
        subject: document.forms["compose-form"]["compose-subject"].value,
        body: document.forms["compose-form"]["compose-body"].value
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      if(result.error === undefined)
      {
        alertnewMailForm(result.message, true) 
        setTimeout(() => load_mailbox("sent"), 1000);
      }
      else
        alertnewMailForm(result.error);  
      
  }).catch(error => {
    console.log('Error:', error);
  });

  return false
}

function alertnewMailForm(message, succes)
{
  document.querySelector('#compose-errmsg').style.display = 'block';
  document.querySelector('#compose-errmsg').innerHTML = message;

  if(succes)
    document.querySelector('#compose-errmsg').classList.replace("alert-danger", "alert-success")
  else
    document.querySelector('#compose-errmsg').classList.replace("alert-success", "alert-danger")
}


function fillEmailsView(emails)
{
    document.querySelector('#emails-list').innerHTML = "";
    document.querySelector('#emails-show').style.display = "none";
    document.querySelector('#emails-emptytext').style.display = "none";
    
    // fill emails list
    let mailListUL = document.createElement('ul')
    mailListUL.classList.add("list-group", 'list-group-flush')

    emails.forEach(email => {
      let li = document.createElement("li")
      li.classList.add("list-group-item")
      
      li.onclick = onMailClicked;
      li.innerHTML = email.subject === "" ? "(No subject) from " + email.sender : email.subject;
      li.dataset.mid = email.id;

      if(email.read)
        li.style.backgroundColor = "lightgrey"

      mailListUL.appendChild(li)
    });
    
    document.querySelector('#emails-list').appendChild(mailListUL)
    
    if(emails.length === 0)
    {
      document.querySelector('#emails-emptytext').style.display = "block";
      document.querySelector('#archive-btn').style.display = "none"
      document.querySelector('#reply-btn').style.display = "none"
      shownMailID = -1;
      return;
    }
    else
    {
      document.querySelector('#reply-btn').style.display = "inline-block"
      showEmail(emails[0])
    }
}

function onMailClicked()
{
  fetch('/emails/' + this.dataset.mid)
    .then(response => response.json())
    .then(email => {
        showEmail(email)
  });
}

function showEmail(email)
{
  console.log(email)
  document.querySelector('#emails-show').style.display = "inline-block";
  document.querySelector('#emails-sender').innerHTML = email.sender
  document.querySelector('#emails-recipients').innerHTML = email.recipients
  document.querySelector('#emails-subject').innerHTML = email.subject
  document.querySelector('#emails-body').innerHTML = email.body
  document.querySelector('#emails-date').innerHTML = email.timestamp

  if(!email.read)
  {
    markAsRead(email)
  }

  shownMailID = email.id;
  shownMail = email;
}

function markAsRead(email)
{
    // send server read info

    fetch('/emails/' + email.id, {
      method: 'PUT',
      body: JSON.stringify({
          read: true
      })
    })

    // update mail in ui
    document.querySelectorAll('li').forEach(elem => {
      if(elem.dataset.mid == email.id)
          elem.style.backgroundColor = "lightgrey"
    })
    
}

function archiveShownMail()
{
  if(shownMailID === -1)
    return

  let archivedVal = currentMailBox === "inbox";
  fetch('/emails/' + shownMailID, {
    method: 'PUT',
    body: JSON.stringify({
        archived: archivedVal
    })
  })

  load_mailbox('inbox')
}

function replyShownMail()
{
  if(shownMailID === -1)
    return

  compose_email()

  // prefill recipient
  let recipient = currentMailBox === "sent" ? shownMail.recipients : shownMail.sender;
  document.querySelector('#compose-recipients').value = recipient

  //Pre-fill the subject line. If the original email had a subject line of foo, the new subject line should be Re: foo. (If the subject line already begins with Re: , no need to add it again.)
  let subject = shownMail.subject.startsWith("Re: ") ? shownMail.subject : "Re: " + shownMail.subject;
  document.querySelector('#compose-subject').value = subject

  //Pre-fill the body of the email with a line like "On Jan 1 2020, 12:00 AM foo@example.com wrote:" followed by the original text of the email.
  let bodyPrefix = `\n\n On ${shownMail.timestamp} ${shownMail.sender} wrote:\n\n${shownMail.body}`;
  document.querySelector('#compose-body').value = bodyPrefix
  
}

