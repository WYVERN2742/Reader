""" A simple reader for online forum posts. """
import sys

import central
import central.uux
import central.net
import central.parse
import central.env

VERSION = 1

def main(url: str) -> None:
	"""A simple reader for online forum posts"""
	url = central.net.normalize_url(url)
	def end():
		central.uux.show_info("End of story")
		central.uux.show_section()
		central.uux.show_info(lastUrl)

	while url is not None:
		central.uux.clear_term()

		lastUrl = url
		central.uux.show_info("URL: " + url)

		content = central.parse.get_story_url_content(url)

		if content is None:
			end()
			return

		index = central.uux.select_content(content)
		nextpage = True

		while nextpage:

			if index == len(content) - 1:
				nextpage = False

			tree = content[index].split("\"")

			central.uux.show_section()

			if not central.uux.display_page(tree, 100):
				end()
				return

			index += 1

		url = central.parse.get_next_story(url)
	end()

# Main program start
if __name__ == "__main__":
	central.uux.show_success("Reader.py v" + str(VERSION))
	url = central.uux.get_args_url(sys.argv, 2)
	try:
		# Suppress debug messages
		central.uux.UUXDEBUG = False

		main(url)
	except KeyboardInterrupt:
		central.uux.show_section()
		central.uux.show_info(url)
	except Exception:
		central.uux.show_stack_trace()
