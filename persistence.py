import shelve
import hashlib
DB_NAME = 'cache'

def hash_jql(jql):
    return hashlib.sha224(jql).hexdigest()

def has_ticket(issue_str):
    db = shelve.open(DB_NAME)
    if not db.has_key(issue_str):
        return False
    else:
        return True

def lookup_ticket(issue_str):
    db = shelve.open(DB_NAME)
    return db[issue_str]

def save_ticket(issue_str, issue):
    db = shelve.open(DB_NAME)
    db[issue_str] = issue
    db.close()

def has_query(jql):
    db = shelve.open(DB_NAME)
    if db.has_key(hash_jql(jql)):
        return True
    else:
        return False

def lookup_query(jql):
    db = shelve.open(DB_NAME)
    return db[hash_jql(jql)]

def save_query(jql, issues):
    db = shelve.open(DB_NAME)
    db[hash_jql(jql)] = issues
    db.close()