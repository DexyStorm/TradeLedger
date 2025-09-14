import praw
import sqlite3
import secret
from secret import *

def give_points(original_poster, deal_partner):
	print(original_poster, "and", deal_partner, "both get one point")

def handle_comment(found_confirmation, user_counter, found_original_poster, deal_partner, original_poster):
	if(found_confirmation == True):
		if(user_counter >= 2):
			print("Multiple trade partners detected.")
			print("You can only announce a trade with one person per comment.")
			print("Please make a separate comment for each trading partner.")
		elif((user_counter == 0) and (found_original_poster == False)):
			print("Could not find trade partner. Please report this to the Admins.")
		elif((user_counter == 0) and (found_original_poster == True)):
			print("It seems like OP has tagged himself in his comment")
			print("You cannot trade with yourself.")
		else:	
			give_points(original_poster, deal_partner)
			print("Your deal partner is:", deal_partner)



def scan_comment(text):

	deal_partner: str = ""

	original_poster: str = comment.submission.author #gets OPs name
	user_counter: int = 0
	found_confirmation: bool = False
	found_original_poster: bool = False

	for elem in text.split():
		if(elem == "!confirm"):
			found_confirmation = True
		if(elem.startswith("u/")):
			if(elem == bot_username):
				continue
			elif(original_poster == elem):
				found_original_poster = True
				continue
			else:
				deal_partner = elem
				user_counter = user_counter + 1

	handle_comment(found_confirmation, user_counter, found_original_poster, deal_partner, original_poster)


if __name__ == "__main__":
	print("test")

	

	reddit_instance = praw.Reddit(username=bot_username, password=password, client_id=client_id, client_secret=client_secret, user_agent=user_agent)

	subreddit = reddit_instance.subreddit(subreddit_name)



	#database stuff





	#main loop starts here
	for comment in reddit_instance.subreddit(subreddit_name).stream.comments(skip_existing=True):
		text: str = comment.body.strip().lower()
		scan_comment(text)
		#
		
	

	
	
	

	