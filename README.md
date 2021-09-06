#Introduction
The Django Rest Chat API provides users with the ability to create conversations with one or more other existing users.

Conversations hold messages, hence please create a conversation first, and to then be able to add messages.

For testing purposes some users have been preconfigured in environments. Please don't forget to authenticate them and update the token variables - see Authentication section below

The API is available on Heroku at:
* https://dj-chat-messages.herokuapp.com/

For admin login:
* https://dj-chat-messages.herokuapp.com/admin/

#Constraints:

* Users can only access objects if they are authenticated, please see the authentication section below.
* Conversations and Messages are only returned to the user if he is either the creator or a recipient of the same, or for Conversations within the recipients of its messages.
* Message recipients are read only! Reading a message will update the date_read of the Recipient object.

#Work flow
* Create a conversation
* Add messages from different users
* Read the messages and mark them as read by doing so (date_read will be populated for the reading recipient)

#Authentication
* Call {{base_url}}/api-token-auth/ with basic authentication (username and password)
* For all other requests use the Token provided by api-token-auth.
* Note that the correct way to set the token is Token <token str>

# Error codes
* For Security Reasons both Not Found and Forbidden will return 404 NOT FOUND For GET list requests, if nothing is found an empty array will be returned

# To set up locally:

** SET `DJANGO_SETTINGS_MODULE=django_rest_chat.{environment}_settings` in your environment variables **:
- don't forget to change the 'environment':
  - terminal: `export DJANGO_SETTINGS_MODULE=django_rest_chat.{environment}_settings`

** add or update secret key files or paths according to {environment} config **