#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
import argparse
import os
import logging
import datetime
import json

logging.basicConfig(
	filename="logfile.log",
	filemode="w",
	format="[%(levelname)s] %(asctime)s - line %(lineno)s - %(message)s",
	level=logging.INFO)

# -----------------------------------------------------------------------
# Default variables

default = "notes"
fp = default + ".json"
wdir = os.path.dirname(os.path.realpath(__file__))
logging.debug(f"Working directory: {wdir}")

# -----------------------------------------------------------------------

class Notebook:
	"""
	Defines a Notebook object."""

	def __init__(self, title=default, path=None, notes=[], last_updated=None):
		self.title = title
		if path is None:		
			self.path = os.path.join(wdir, title + ".json")
		else:
			self.path = path
		self.notes = notes
		self.last_updated = last_updated
		
	def update_changes(self):
		"""
		Updates unsaved changes to file.
		This method should be called whenever a change is made."""

		# Fix for notes ids getting messed up when removing a note
		for note in self.notes:
			note_index = self.notes.index(note) + 1
			if note["id"] != note_index:
				note["id"] = note_index
		
		# Update JSON file
		data = self.__dict__
		logging.debug(f"Data to be written: '{data}'")

		with open(self.path, "w", encoding="utf-8") as f:
			json.dump(data, f, indent=2)
			logging.info("Sucessfully updated file")

		"""except Exception as e:
			logging.error(f"couldn't update json file: {e}")
			print(f"'{self.title}' notebook couldn't be updated ({e})")"""

	def get_note(self, note_id):
		"""Returns a note with index N."""

		if self.notes:
			if note_id > 0: note_id -= 1
			try:
				note = self.notes[note_id]
				logging.info(f"Getting note with id {note_id}")
				return note
			except IndexError:
				logging.error(f"A note with id ({note_id}) was not found")
				print(f"Note ({note_id+1}) not found.")
		
	def current_time(self):
		"""Get current time."""

		return datetime.datetime.now()
	
	def create_note(self, content, title=None):
		"""Creates a new note."""

		note_id = 1 if not self.notes else len(self.notes) + 1
		created = self.current_time().strftime("%Y%m%d%H%M%S")
		title = "Untitled" if title is None else title[0]
		content_data = {"id": note_id, "created": created, "title": title, "content": content}

		self.notes.append(content_data)
		self.last_updated = content_data["created"]
		print("Note created.")
		self.update_changes()
	
	def edit_note(self, note_id):
		"""Edits a note with index N."""

		note = self.get_note(note_id)
		if note:
			try:
				note["title"] = input("New title: ")
				if not note["title"]:
					note["title"] = "Untitled"
				note["content"] = input("Note:\n")
				print("Note edited.")
				note["last_edited"] = self.current_time().strftime("%Y%m%d%H%M%S")
				self.update_changes()
			except KeyboardInterrupt:
				print("\nAborting.")
	
	def read_note(self, note_id, card=False):
		"""Reads a note with index N."""

		note = self.get_note(note_id)
		if note:
			index, text, title = note["id"], note["content"], note["title"]
			edited = note["created"] if not "edited" in note.keys() else note["edited"]
			last_edited = datetime.datetime.strptime(edited, "%Y%m%d%H%M%S")
			time = last_edited.strftime("%Y-%m-%d, %H:%M")

			if card:
				"""
				If running using note index, i.e. "cup.py rd 1",
				it will print the full content.

				---------------------------------------------
				Title
				-----
				This is an example and contains a title.
				
				Last edited: 2022-05-27, 21:59.
				---------------------------------------------
				"""
				print(f"{title}")
				print("-" * len(title))
				print("".join(text))
				if text and not text[len(text)-1].endswith("\n"):
					print()
				print(f"Last edited: {time}.")

			else:
				"""
				By default, it will print notes in list view.
				-----------------------------------------------
				[1] 2022-05-27, 21:59 - This is another example
				-----------------------------------------------
				"""

				if title == "Untitled":
					if "\n" in text:
						text = text.splitlines()[0] + "(...)"
					title = text

				print(f"[{index}] {time} - {title}")

	def show_notes(self):
		"""Prints notes to the terminal."""

		if self.notes:
			print("Your notes:")
			for i in range(1, len(self.notes)+1):
				self.read_note(i)
		else:
			print("You don't have any notes yet.")
			print(f"Try adding a note with 'cup.py add [note]'")
		
	def delete_note(self, note_id):
		"""Deletes a note with index N."""

		note = self.get_note(note_id)
		if note:
			logging.info(f"Removing note ({note_id})")
			self.notes.remove(note)
			self.update_changes()
			self.show_notes()

def load_notebook():
	"""Check if a notebook already exists."""
	if os.path.exists(fp):
		with open(fp, "r") as filepath:
			content = filepath.read()
		return json.loads(content)
	else:
		return None

def get_args():
	parser = argparse.ArgumentParser(prog="cup", description="A simple command-line note manager.")
	subparser = parser.add_subparsers(dest="com")

	add = subparser.add_parser("add", help="creates a new note")
	add.add_argument("text", nargs="?", help="note's content")
	add.add_argument("-t", nargs="+", help="note's title")

	ed = subparser.add_parser("ed", help="edits a note")
	ed.add_argument("id", type=int, help="note's ID")
	rd = subparser.add_parser("cat", help="reads a note")
	rd.add_argument("id", type=int, help="note's ID")
	rm = subparser.add_parser("rm", help="removes a note")
	rm.add_argument("id", type=int, help="note's ID")

	args = parser.parse_args()
	return args

def main():

	# Check if a notebook already exists in directory
	data = load_notebook()
	if data is None:
		n = Notebook()
	else:
		n = Notebook(**data)

	if len(sys.argv) == 1:
		n.show_notes()
	else:
		args = get_args()
		if args.com == "add":
			text, title = args.text, None if not args.t else args.t
			n.create_note(text, title)
			n.show_notes()
		
		elif args.com in ["cat", "ed", "rm"]:
			funcs = {
				"cat": n.read_note,
				"ed": n.edit_note ,
				"rm": n.delete_note }
			if args.com == "cat":
				funcs[args.com](note_id=args.id, card=True)
			else:
				funcs[args.com](note_id=args.id)

if __name__ == "__main__":
	main()