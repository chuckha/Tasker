from random import choice
from string import lowercase

def dict_to_plist(dictionary):
    plist = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">\n"""
    plist += "  <dict>\n"
    for key, value in dictionary.iteritems():
        plist += "    <key>%s</key>\n" % key
        plist += "%s" % val_to_plist_val(value)
    plist += "  </dict>\n"
    plist += "</plist>"
    return plist

def val_to_plist_val(val, indent=2):
    spaces = "  " * indent
    if isinstance(val, str):
        return "%s<string>%s</string>\n" % (spaces, val)
    elif isinstance(val, int):
        return "%s<integer>%s</integer>\n" % (spaces, val)
    elif isinstance(val, list):
        return "%s<array>\n%s%s</array>\n" % (spaces, "".join([val_to_plist_val(v, indent+1) for v in val]), spaces)



if __name__=="__main__":
    print dict_to_plist({"Label": "Bananas", "StartInterval": "sup"})
    print dict_to_plist({"ProgramArguments": ["echo", "hello world"]})
    print dict_to_plist({"ProgramArguments": [[1,2,3], "b", [1,2,4]]})
