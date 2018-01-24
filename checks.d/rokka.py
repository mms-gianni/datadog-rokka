import json
from urllib2 import Request, urlopen, URLError
from checks import AgentCheck

class Rokka(AgentCheck):
    APIURL = 'https://api.rokka.io/stats'

    def __init__(self, name, init_config, agentConfig, instances=None):

        AgentCheck.__init__(self, name, init_config, agentConfig, instances=instances)

    def check(self, instance):

        if instance.get("organisation", None) is None:
            raise Exception("add a organisation")
        organisation = instance.get('organisation')

        apikey = self.init_config.get('rokka_api_key')

        url = self.APIURL+'/'+organisation

        request = Request(url, headers={"Api-Key" : apikey})

        # Load the data
        try:
            response = urlopen(request)
            res = json.loads(response.read())
        except URLError, e:
            print 'ERROR: ', e

        # format the data
        data = {
             "space_in_bytes": res['space_in_bytes'][0]['value'],
             "number_of_files": res['number_of_files'][0]['value'],
             "bytes_downloaded": res['bytes_downloaded'][0]['value'],
           }

        # send the data
        try:
            for field, value in data.iteritems():
                # self.log.debug(data)
                tags = ['organisation:%s' % organisation]
                self.gauge('rokka.'+field, value, tags=tags)
        except ValueError:
            self.log.error("Failed to save data")
            return