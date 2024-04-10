import base64
import requests

def encode_base64(fName):
    with open(fName, 'rb') as file:
        binary_file_data = file.read()
        base64_encoded_data = base64.b64encode(binary_file_data)
        return base64_encoded_data.decode('utf-8')

def decode_Base64(fName, data):
    data_base64 = data.encode('utf-8')
    with open(fName, 'wb') as file:
        decoded_data = base64.decodebytes(data_base64)
        file.write(decoded_data)


if __name__ == '__main__':
    enc = encode_base64('flask_fotoserver/img/turm.jpg')
    decode_Base64('/tmp/img.png', enc)

    j = {'name': 'Eiffelturm', 'ext': 'jpg', 'data': enc, 'desc': 'Foto vom Eiffelturm'}
    response = requests.put('http://localhost:5000/img_meta/10' , json=j)
    print(response.text)

    response = requests.get('http://localhost:5000/img_meta/1')
    res_json = response.json()
    print(res_json)
    decode_Base64('flask_fotoserver/tmp/' + res_json['name'] + "_server." + res_json['ext'], res_json['data'])
    
    
    response = requests.delete('http://localhost:5000/img_meta/1')
    print(response.text)
    
    
    response = requests.get('http://localhost:5000/img_meta/1')
    res_json = response.json()
    print(res_json)
    
    response = requests.get('http://localhost:5000/img_meta/search/Eiff')
    res_json = response.json()
    for image in res_json:
        print(image['name'])
    
    