from boo.year import make_url
from boo.path import raw, processed

# message system

def filesize(path):
    return round(path.stat().st_size / (1024 * 1024.0), 1)

    
def help_download_force(year):
    return f"Use download({year}, force=True) to overwrite existing file."


def help_build_force(year):
    return f"Use build({year}, force=True) to overwrite existing file."


def help_download(year):
    return f"Use download({year}) to download raw CSV file."


def help_build(year):
    return f"Use build({year}) to create readable file."


def help_df(year):
    return f"Use df = read_dataframe({year}) to read it as pandas dataframe."


     
class Dataset:    
    def __init__(self, year):
        self.year = year
        self.url = make_url(year)
        self.raw = raw(year)
        self.processed = processed(year)
        
    def is_downloaded(self):
        return self.raw.exists()
    
    def is_built(self):
        return self.processed.exists() 
    
    def raw_state(self):
        if self.is_downloaded():            
            size = filesize(self.raw)
            yield f"Raw CSV file downloaded as {self.raw} ({size}M)"
            if size < 1:
                yield "WARNING: file size too small. " + help_download_force(self.year)
        else:
            yield "Raw CSV file not downloaded. " + help_download(self.year)                
                
    def processed_state(self):
        if self.is_built():
            size = filesize(self.processed)
            yield f"Processed CSV file is saved as {self.processed} ({size}M)"
            yield help_df(self.year)
        else:
            yield "CSV file not built. " + help_build(self.year)
            

def inspect(year: int):
    d = Dataset(year)
    print ("Raw file URL:", d.url)
    for msg in d.raw_state():
        print (msg)
    for msg in d.processed_state():
        print (msg)  
                        