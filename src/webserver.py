# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import time
from transformers import AutoTokenizer,AutoModelForCausalLM

hostName = "localhost"
serverPort = 8080

#tokenizer = AutoTokenizer.from_pretrained("bigscience/bloom-560m", device_map="auto", cache_dir="/mnt/qb/work2/mlcolab0/mqw155/cache/")
#model = AutoModelForCausalLM.from_pretrained("bigscience/bloom-560m", cache_dir="/mnt/qb/work2/mlcolab0/mqw155/cache/")

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        global model, tokenizer
        parsed_qs = parse_qs(self.path)
        text_prompt = parsed_qs.get('/?prompt', ['I want to break free'])[0]
        print(text_prompt)
        inputs = tokenizer(text_prompt, return_tensors="pt").input_ids
        result = model.generate(inputs,max_length=200,top_k=0,temperature=0.5)
        output = tokenizer.decode(result[0], truncate_before_pattern=[r"\n\n^#","^'''","\n\n\n"])
        print(output)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>" + output + "</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")