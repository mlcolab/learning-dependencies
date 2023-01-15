from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from transformers import AutoTokenizer, AutoModelForCausalLM
import json
import time

hostName = "localhost"
serverPort = 8101
device = 'cpu'

tokenizer = AutoTokenizer.from_pretrained("facebook/galactica-125m", device_map="auto")
model = AutoModelForCausalLM.from_pretrained("facebook/galactica-125m").to(device)
#, cache_dir="/mnt/qb/work2/mlcolab0/mqw155/cache/"

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        start_time = time.time()
        global model, tokenizer
        parsed_qs = parse_qs(self.path)
        text_prompt = parsed_qs.get('/?prompt', ['I want to break free'])[0]

        inputs = tokenizer.encode(text_prompt, return_tensors="pt").to(device)
        results = model.generate(inputs, min_length=30, max_length=200)
        output = tokenizer.batch_decode(results, skip_special_tokens=True)

        data = {'response': output, 'time': time.time() - start_time}
        json_data = json.dumps(data)

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json_data.encode())

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
