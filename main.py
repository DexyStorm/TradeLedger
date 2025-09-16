import praw
import sqlite3
import secret
import re
from secret import *

def give_points(original_poster, deal_partner):
	print(original_poster, "and", deal_partner, "both get one point")


def sanitize_traded_text(text):
	text = text.replace(' u/TradeLedger ', '')
	text = text.replace('u/TradeLedger ', '')
	text = text.replace(' u/TradeLedger', '')
	return text

def get_username_from_mention(text):

	if(text.startswith("u/")):
		return text

	finished_str: str = ""

	text = text [::-1]

	#print("\n")

	first: bool = True
	second: bool = True

	for elem in text:
		if(first == True):
			first = False
		elif(second == True):
			second = False
		elif(elem == "/"):
			break
		else:
			finished_str = finished_str + elem

	finished_str = finished_str [::-1]
	finished_str = "u/" + finished_str
	return finished_str
	

def handle_traded(text):

	comment_original_poster: str = comment.author #gets the name of comment OP
	comment_original_poster = "u/" + comment_original_poster.name
	found_original_poster = False
	user_counter: int = 0

	for elem in text.split():
		if(elem.lower().startswith("[u/") or elem.lower().startswith("u/")):
			trade_partner = get_username_from_mention(elem)

			if(comment_original_poster.lower() == trade_partner.lower()):
				found_original_poster = True
				continue
			elif(trade_partner.lower() == ("u/" + bot_username.lower())):
				continue
			
			else:
				#print("comment_original_poster:", comment_original_poster)
				#print("trade_partner: ", trade_partner)
				user_counter = user_counter + 1


	if(user_counter >= 2):
		print("Multiple trade partners detected.")
		print("You can only announce a trade with one person per comment.")
		print("If you have traded with multiple people, please make a separate comment for each trading partner.\n")
	elif((user_counter == 0) and (found_original_poster == False)):
		print("Could not find trade partner. Please report this to the Admins.\n")
	elif((user_counter == 0) and (found_original_poster == True)):
		print("It seems like OP has tagged himself in his comment")
		print("You cannot trade with yourself.\n")
	else:	
		give_points(comment_original_poster, trade_partner)
		print("Your deal partner is:", trade_partner, "\n")


	#debug:
	#print("found_original_poster: ", found_original_poster)
	#print("comment_original_poster: ", comment_original_poster)
	#print("user_counter: ", user_counter)
	#print("deal_partner: ", deal_partner)



def handle_confirm(text):
	text: str = sanitize_traded_text(text)

	#todo: 
	#put in database

def check_if_comment_op_is_op(comment):
	if(comment.author == comment.submission.author):
		return True
	else:
		return False

def parse_comment(text, comment):

	if(text.lower().startswith("!sold") or text.lower().startswith("!sell") or text.lower().startswith("!traded") or text.lower().startswith("!trade")):
		if(check_if_comment_op_is_op(comment) == True):
			handle_traded(text)
		else:
			print("Sorry, only the original poster can initiate a confirmation.\n")
	elif(text.lower().startswith("!confirm")):
		handle_confirm(text)







if __name__ == "__main__":
	
	reddit_instance = praw.Reddit(username=bot_username, password=password, client_id=client_id, client_secret=client_secret, user_agent=user_agent)
	print("")

	subreddit = reddit_instance.subreddit(subreddit_name)



	#database stuff





	#main loop starts here
	for comment in reddit_instance.subreddit(subreddit_name).stream.comments(skip_existing=True):
		text: str = comment.body.strip().lower()

		
		parse_comment(text, comment)



		
		#
		
	

	
	
	

	