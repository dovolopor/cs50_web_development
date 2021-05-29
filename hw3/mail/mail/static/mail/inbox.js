document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').onsubmit = sendMail;

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
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
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