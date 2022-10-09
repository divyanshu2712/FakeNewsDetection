# It is the python file imported by app.py to enable to store only the secure passwords
def password_2(s):
    '''A function which checks the given string the following:
    1: Does it has a character of upper case
    2: Does it has a character of lower case
    3: Does it contain digit
    4: Does it contain Special Character
    A secure password should atleast meet all this requirements
    Returns:
    It will return true it password is secure
    Else:
    Returns False'''
    special='[@_!$%^&*()<>?/\|}{~:]#'
    digit='1234567890'
    low_alphabet='abcdefghijklmnopqrstuvwxyz'
    upper_alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ' 
    f1=0
    f2=0
    f3=0
    f4=0
    for i in s:
        if i in low_alphabet:
            f1=f1+1
        if i in upper_alphabet:
            f4=f4+1
        if i in digit:
            f2=f2+1
        if i in special:
            f3=f3+1
    if f1>0 and f2>0 and f3>0 and f4>0:
        return True
    else:
        return False