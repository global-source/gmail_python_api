import json
import base as b
import numpy as np
import os
import service_utils


class MailService(service_utils.ServiceUtils):
    """
    Base Mail services for GMail API.
    """

    # Default user to process.
    user = None
    # Service instance from GMail
    service = None
    # Sample data
    sample_data = []
    # Sender List
    senders = []
    # Search Query to filter Mails
    search_query = ''
    # Sender name to filter FROM mail
    sender_name = ''
    # Default senders list file location
    sender_list_file = 'data/sender_list.json'
    # Default mail ID source file location
    mail_source_file = 'data/mail_ids.json'

    def __init__(self, **kwargs):
        """
        Setup the App to start 
        """
        # Set 'service' instance from GMail API
        self.service = b.main()

    def fetch_mails(self):
        """
        This will load all or based on search query.
        """
        try:
            file_name = self.get_mails_file_name(
                search_query=self.search_query)
            _mail_ids = b.ut.ListMessagesMatchingQuery(
                self.service, self.user, self.search_query)
            with open(file_name, 'w') as f:
                f.write(str(_mail_ids))
            return True
        except Exception as e:
            print(str(e))
            return False

    def load_mails(self, count=10):
        try:
            with open(self.mail_source_file) as _file:
                data = json.loads(_file.read())
            return data[:count]
        except Exception as e:
            print(str(e))

    def fetch_and_store_senders(self):
        try:
            _list = []
            items = self.load_mails(count=1000)
            profiles = np.array_split(items, 50)
            batch = 1
            for i in profiles:
                _list = self.filter_by_sender(data=i)
                self.senders = _list
                self.store_senders(append=True)
                print('Batch :%d | Stored Successfully !' % batch)
                batch += 1
        except Exception as e:
            print(str(e))

    # def load_sender_profiles(self, count=10, store=False):
    #     try:
    #         _list = []
    #         profiles = self.load_mails(count=count)
    #         _list = self.filter_by_sender(data=profiles)
    #         self.senders = _list
    #         self.store_senders(append=store)
    #         return self.senders
    #     except Exception as e:
    #         print(str(e))

    def filter_by_sender(self, data):
        try:
            _list = []
            for i in data:
                mail = b.ut.GetMessage(
                    self.service, self.user, i['id'])
                value = self.parse_sender(mail=mail)
                if None != value:
                    if(value.find(self.sender_name) != -1):
                        _list.append({'mail_id': value, 'id': i['id']})
            return _list
        except Exception as e:
            print(str(e))

    def store_senders(self, append=False):
        try:
            file_open_type = 'w'
            if append:
                file_open_type = 'w+'
            file_name = self.get_sender_file_name(sender_name=self.sender_name)

            if None != self.senders:
                if len(self.senders):
                    with open(file_name, file_open_type) as f:
                        f.write(str(self.senders))

            return True
        except Exception as e:
            print(str(e))

    def parse_sender(self, mail):
        try:
            return mail['payload']['headers'][7]['value']
        except Exception as e:
            print(str(e))
