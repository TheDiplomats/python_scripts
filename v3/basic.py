import requests
endpoint = "https://wmeasnad71.aepsc.com:8001/ws/AEP_OhioCres_EFYW.ws:EFYW?WSDL"
headers = {'content-type': 'application/xml'}
payload = ''' <?xml version="1.0" encoding="utf-8"?>
 <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://wmeasnad71.aepsc.co/AEP_OhioCres_EFYW.ws:EFYW\">
                   <soapenv:Header/>
                   <soapenv:Body>
                   <tns:getSDIDetail>
                   <tns:EFYWRequest>
                   <tns:tDat>"foo"</tns:tDat>
                   <tns:telephoneNumber>"foo"</tns:telephoneNumber>
                   <tns:lastFourSSN>"foo"</tns:lastFourSSN>
                   <tns:billAmount>"foo"</tns:billAmount>
                  <tns:providerID>"foo"</tns:providerID>
                   </tns:EFYWRequest>
                   </tns:getSDIDetail>
                   </soapenv:Body>
		</soapenv:Envelope> '''
response = requests.get(endpoint, data = xml.data(payload), headers = headers)