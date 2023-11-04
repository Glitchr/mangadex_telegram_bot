

class Chapter:
    def __init__(self, data):
        """Initialize a Chapter object from a data dictionary"""
        
        # get the title attribute
        self.title = data['attributes']['title']
        
        if type(self.title) == dict:
            # try to get the title in English or Japanese
            self.title = self.title.get('en') or self.title.get('ja-ro')
        if self.title is None:
            # if both are missing, get the first available key
            first_key = next(iter(self.title))
            self.title = self.title[first_key]
        else:
            # assume title is already a string
            pass
    
        # use a default value if title is still None or empty 
        self.title = self.title or 'Title not available'
        
        # get other attributes you want 
        self.chapter_number = data['attributes']['chapter']
        self.volume_number = data['attributes']['volume']
        self.chapter_id = data['id']

         
    def print_info(self):
        """Print the information of this Chapter object"""
    
        print(f"Title: {self.title}")
        print(f"Chapter: {self.chapter_number}")
        print(f"Volume: {self.volume_number}")
        print(f"Link: https://mangadex.org/chapter/{self.chapter_id}")
