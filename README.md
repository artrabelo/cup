# ☕ cup

A simple note manager for command-liners.

It's a project still in development and it is yet to mature, so feel free to leave your comments.

## Getting started

`cup` does not requires installation or additional requirements and it works out-of-the-box.

### How to use it

>*The human whose name is written on this note shall... have a coffee?*

#### Basic commands

Running cup without arguments will show your saved notes or a quick tutorial if you don't have any notes yet.

Creating a new note is as easy as `cup add [your note]`. This is the simplest way to work with cup. You can also provide a title with `-t`.

```console
~$ cup.py add "This looks like an article!" -t "First blog post"
Note created.

(1) 2022-01-26 - First blog post
```

You can also add a multiline text by pressing `Enter` or `Return` in the terminal after a open quotation mark.

```console
~$ cup.py add "The moth don't care
> when he
> sees the flame"
```

To read, edit and delete a note, cup uses console-friendly words such as `cat`, `ed` and `rm`, respectively.

```console
~$ cup.py cat 1

First blog post
---------------
This looks like an article!

Last updated: 2022-01-26, 18:13.
```

#### What it eats

`cup` uses a JSON file to store notes. This makes it easy to group your notes by topic and import/export them. It looks like this:

```json
{
	"notebook": "main",
	"last_updated": 20220126141024,
	"path": "path/to/notes.json",
	"notes": [
		{
			"id": 1,
			"created": 20220126141024,
			"title": "Example", 
			"text": "First note"
		}
	]
}
```

### To-do

* Add support for to-do lists
* Add support for text files