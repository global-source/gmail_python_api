class ServiceUtils():
   def get_sender_file_name(self, sender_name):
        try:
            file_name = str(sender_name)
            file_name = file_name.replace('.', '_')
            file_name = file_name.replace('-', '_')
            file_name = file_name.replace('@', '_')

            return 'data/' + file_name + '_sender.json'
        except Exception as e:
            print(str(e))

    def get_mails_file_name(self, search_query):
        try:
            file_name = str(search_query)
            file_name = file_name.replace('.', '_')
            file_name = file_name.replace('-', '_')
            file_name = file_name.replace('@', '_')

            return 'data/' + file_name + '_mails.json'
        except Exception as e:
            print(str(e))
