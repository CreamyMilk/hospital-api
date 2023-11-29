import africastalking
from flask import Flask,request

app = Flask(__name__)

# AfricasTalkingAPI stuff
username = "tenn_fund_users"    # use 'sandbox' for development in the test environment
api_key = "6b94da223b14cb836f8b134bbe74bc120d0c1b96b04afb52a8af193b37296c00"      # use your sandbox app API key for development in the test environment

africastalking.initialize(username, api_key)

sms = africastalking.SMS

users = []

def sendQueueMessage(user,next=False):
    message = ""
    if next:
        message = f'Hello {user["username"]}, its your turn to be served. Your reference number is {user["number"]}'
    else:  
        message = f'Hello {user["username"]}, you have been assigned NO: "{user["number"]}". \n Will Text you when its your turn to get served'
    print("🚀sending " + message)
    try:
        response = sms.send(message, [user["phone"]])
        print(response)
    except:
        print("❌ issue with message sending")


@app.route("/registeruser",methods=['POST'])
def register_user():
    data =  request.json

    queueNumber = len(users)+1
    
    newUser = {
        "number" : queueNumber,
        "phone":data.get("phone"),
        "email":data.get("email"),
        "username":data.get("username"),
        "served" : False
    }

    users.append(newUser)

    sendQueueMessage(newUser)
    
    print(data)

    return users


@app.route("/serveUsers",methods=['POST'])
def server_user():
    data = request.json
    pos = data.get("number") - 1
    print(users[pos])
    users[pos]['served'] = True
    if len(users) > pos+1:
        if users[pos+1]['served'] == False:
            sendQueueMessage(users[pos+1],True)
    return users[pos]



@app.route("/listUsers",methods=['GET'])
def list_users():
    return users



