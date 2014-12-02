## This is by our Multicorn ForeignDataWrapper to convert strings with PostgreSQL operators in them to functions.
## R.Otten - 2014

import operator
import re

## We throw this if we encounter an operator that we don't know what to do with:
class unknownOperatorException(Exception):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


################################################################################
### Custom functions to implement some of the operators:
def reverseContains(a, b):
    return operator.contains(b, a)

def strictlyLeft(a, b):
    return max(a) < min(b)

def strictlyRight(a, b):
    return min(a) > max(b)

def rightBounded(a, b):
    return max(a) <= max(b)

def leftBounded(a, b):
    return min(a) >= min(b)

def overlap(a, b):
    if (min(a) >= min(b)) and (min(a) <= max(b)):
        return True
    if (max(a) <= max(b)) and (max(a) >= min(b)):
        return True
    return False

def regexSearch(a, b):
    if re.search(b, a):
        return True
    else:
        return False

def regexSearch_i(a, b):
    if re.search(b, a, re.I):
        return True
    else:
        return False

def notRegexSearch(a, b):
     return not regexSearch(a, b)

def notRegexSearch_i(a, b):
     return not regexSearch_i(a, b)

def likeSearch(a, b):
    b.replace('%%', '.*')
    b.replace('_', '.')
    return regexSearch(a, b)

def likeSearch_i(a, b):
    b.replace('%%', '.*')
    b.replace('_', '.')
    return regexSearch_i(a, b)

def notLikeSearch(a, b):
    b.replace('%%', '.*')
    b.replace('_', '.')
    return not regexSearch(a, b)

def notLikeSearch_i(a, b):
    b.replace('%%', '.*')
    b.replace('_', '.')
    return not regexSearch_i(a, b)


################################################################################
### The main function we use external to this file:
## Translate a string with an operator in it (eg. ">=") into a function.
##
## Not supported (yet -- feel free to add more support!):
##    "between" -- it isn't clear if we'll get those.
##    "OR"      -- it isnt' clear if we'll get those.
##    Geometric Operators
##    Text Search Operators
##    Network Address Operators
##    JSON Operators
##    The Array operators when used on Ranges
## 
def getOperatorFunction(opr):

  operatorFunctionMap = {
      '<':          operator.lt,
      '>':          operator.gt,
      '<=':         operator.le,
      '>=':         operator.ge,
      '=':          operator.eq,
      '<>':         operator.ne,
      '!=':         operator.ne,
      '@>':         operator.contains,
      '<@':         reverseContains,
      '<<':         strictlyLeft,
      '>>':         strictlyRight,
      '&<':         rightBounded,
      '>&':         leftBounded,
      '&&':         overlap,
      'is':         operator.eq, # this one won't work in every sql context, but should for some cases
      '~':          regexSearch,
      '~*':         regexSearch_i,
      '!~':         notRegexSearch,
      '!~*':        notRegexSearch_i,
      '~~':         likeSearch,
      '!~~':        notLikeSearch,
      'like':       likeSearch,
      'not like':   notLikeSearch,
      '~~*':        likeSearch_i,
      '!~~*':       notLikeSearch_i,
      'ilike':      likeSearch_i,
      'not ilike':  likeSearch_i,
      'similar to': regexSearch,
      'not similar to': notRegexSearch
  }

  if not operatorFunctionMap.has_key(opr):
      raise unknownOperatorException("'%s' is not a supported operator." % opr)

  return operatorFunctionMap[opr]



