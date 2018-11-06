from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    
    def handle_starttag(self, tag, attrs):
        pass
        # print("Encountered a start tag:", tag)

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        self.setlist.append(data)