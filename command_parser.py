import re

def as_string_requested(command):
    # Find all the qualifiers, e.g. -S -t
    # Then see if -S in it
    qualifiers = re.findall("\s*-\w\s", command.strip())
    as_str = False
    for q in qualifiers:
        if "-S" in q.strip():
            as_str = True
            break
    return as_str


def extract_pv_name(command):
    # Find all the qualifiers, e.g. -S -t
    # We only care about -S at the moment
    ans = re.match("^caget(\s+-\w)*\s+([\w_:]+)[\s|\w]*$", command.strip())
    return ans.groups()[-1]


def uzhex_requested(command):
    ans = re.search("\|\s*uzhex$", command.strip())
    return ans is not None