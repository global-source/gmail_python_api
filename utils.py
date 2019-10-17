
from apiclient import errors
import base64
import email
from apiclient import errors


def ListMessagesMatchingQuery(service, user_id, query=''):
      response = service.users().messages().list(userId=user_id, q=query).execute()
      messages = []
      if 'messages' in response:
            messages.extend(response['messages'])
      while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(
                userId=user_id, q=query, pageToken=page_token).execute()
            messages.extend(response['messages'])
      return messages


def ListMessagesWithLabels(service, user_id, label_ids=[]):
      response = service.users().messages().list(
          userId=user_id, labelIds=label_ids).execute()
      messages = []
      if 'messages' in response:
            messages.extend(response['messages'])
      while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(
                userId=user_id, labelIds=label_ids, pageToken=page_token).execute()
            messages.extend(response['messages'])
      return messages


def DeleteMessage(service, user_id, msg_id):

    try:
        service.users().messages().delete(userId=user_id, id=msg_id).execute()
        print('Message with id: %s deleted successfully.' % msg_id)
    except (errors.HttpError, error):
        print('An error occurred: %s' % error)


def GetMessage(service, user_id, msg_id):

    # try:
    message = service.users().messages().get(userId=user_id, id=msg_id).execute()
    # print('Message snippet: %s' % message['snippet'])
    return message
    # except (errors.HttpError, error):
    #     print('An error occurred: %s' % error)


def GetMimeMessage(service, user_id, msg_id):
  
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id,
                                                 format='raw').execute()

        # print('Message snippet: %s' % message['snippet'])

        msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))

        mime_msg = email.message_from_string(msg_str)

        return mime_msg
    except (errors.HttpError, error):
        print('An error occurred: %s' % error)
