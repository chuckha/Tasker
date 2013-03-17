import re
import os

# glob dir to get files

# given a file
# read through each <dict><key><xxx> pair
# build dict
LAUNCH_AGENT_DIR = os.path.join("%s" % os.environ['HOME'], "Library", "LaunchAgents")

class LaunchdPlistSyntaxException(Exception):
    pass

def print_plist_files():
    files = get_plist_files()
    for f in files:
        print "Filename: %s" % f
        print_plist_dict(build_dict(open(f).read()))

def print_plist_dict(d):
    print "Label: %s" % d["Label"]
    d.pop("Label", None)
    print "Runs every: %s seconds" % d["StartInterval"]
    d.pop("StartInterval", None)
    print "Command: %s" % " ".join(d["ProgramArguments"])
    d.pop("ProgramArguments", None)
    print "-Extra info-"
    for k, v in d.iteritems():
        print "%s: %s" % (k, v)
    print

def get_plist_files():
    # make sure we only get .plist files
    plist_files = [f for f in os.listdir(LAUNCH_AGENT_DIR) if f.endswith('.plist')]
    # and make them full paths
    full_paths = [os.path.join(LAUNCH_AGENT_DIR, p) for p in plist_files]
    return full_paths

def parse_plist_files(plist_files):
    dicts = []
    for plist_file in plist_files:
        contents = open(plist_file).read()
        try:
            dicts.append(build_dict(contents))
        except:
            print("Failure parsing %s" % plist_file)
    return dicts

def interesting_lines(contents):
    yield_all = False
    for line in contents.split('\n'):
        if "<dict>" in line and not yield_all:
            yield_all = True
            continue
        elif "</dict>" in line and yield_all:
            yield_all = False
        elif yield_all:
            yield line

def build_dict(contents):
    d = {}
    current_key = ""
    in_array = False
    for line in interesting_lines(contents):
        key = re.search('<key>(.*)</key>', line)
        sval = re.search('<string>(.*)</string>', line)
        ival = re.search('<integer>(.*)</integer>', line)
        aval = re.search('<array>', line)
        eaval = re.search('</array>', line)
        if key:
            if in_array:
                raise LaunchdPlistSyntaxError("Can't have key in an array")
            current_key = key.group(1)
        if sval:
            s = str(sval.group(1))
            if in_array:
                a.append(s)
            else:
                d[current_key] = s
        if ival:
            i = int(ival.group(1))
            if in_array:
                a.append(i)
            else:
                d[current_key] = i
        if aval:
            in_array = True
            a = []
            continue
        if eaval:
            in_array = False
            d[current_key] = a
            a = []
    return d

if __name__ == "__main__":
    v = """<plist version="1.0">
      <dict>
        <key>ProgramArguments</key>
        <array>
          <string>echo</string>
          <string>cool beans</string>
        </array>
        <key>StartInterval</key>
        <integer>44444</integer>
        <key>Label</key>
        <string>hello world</string>
      </dict>
    </plist>"""
    dicts = parse_plist_files(get_plist_files())
    for d in dicts:
        print_plist_dict(d)
