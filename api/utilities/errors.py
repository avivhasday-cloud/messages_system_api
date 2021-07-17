from werkzeug.exceptions import HTTPException

class InternalServerError(HTTPException):
    pass

class IncorrectUsernameError(HTTPException):
    pass

class IncorrectPasswordError(HTTPException):
    pass

class UsernameAlreadyExistsError(HTTPException):
    pass

class MessageDoesntExistsError(HTTPException):
    pass



errors = {
    "InternalServerError":{
        "status":500,
        "message": 'General Error!'
    },
    "IncorrectUsernameError":{
        "status":400,
        "message": 'Incorrect Username!'
    },
    "IncorrectPasswordError":{
        "status":400,
        "Message": 'Incorrect Password!'
    },
    "UsernameAlreadyExists":{
        'status':409,
        'Message':'User already exists. Please Log in.'
    },
    "MessageDoesntExistsError":{
        'status':404,
        'Message':'Message does not exists'
    },


}