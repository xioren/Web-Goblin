### Usage:

```
usage: image-goblin [OPTIONS] [URL]

positional arguments:
  url                   webpage or image url

optional arguments:
  -h, --help            show this help message and exit
  --best                used in conjunction with --force, overwrites files only if new file size is greater
  -d DELAY, --delay DELAY
                        delay ("-1" for randomized delay), default: 0
  --dir DIR             specify name or path of the download directory. the directory will be created if it does not exist
  --ext EXT             specify which extension(s) to download jpg,png[,...]
  --feed                input urls one at a time
  --filename FILENAME   specify filename to use (will always be made unique for each file)
  --filter FILTER       download only urls containing filter string; can handle regex patterns
  --force               force overwriting existing files
  -f FORMAT, --format FORMAT
                        formatting modifier (action modifier[ replacement]), needs to be quoted
  -g GOBLIN, --goblin GOBLIN
                        use a specific goblin
  --greedy              find urls based on regex instead of html tags (only applies to generic goblin)
  --list                list available goblins
  -l LOCAL, --local LOCAL
                        filename or path of a local text file containing urls
  --login               log in (goblin dependant)
  --mask                use a common user agent header
  --minsize MINSIZE     minimum filesize to download (in bytes), default: 30000 (30kb)
  -m MODE, --mode MODE  mode settings (goblin dependant)
  --nodl                print urls to stdout instead of downloading
  --noskip              make filenames unique if a file with the same name already exists, instead of skipping
  --nosort              download directly to current directory, without creating sub dirs
  --noup                do not remove cropping and scaling from urls
  --posts POSTS         number of posts (n<100) to fetch (goblin dependant)
  -s, --silent          suppress output
  --slugify             slugify filenames
  --step STEP           iteration step size (n)
  -t TIMEOUT, --timeout TIMEOUT
                        consecutive failed attempts threshold (n) during iteration, default: 5
  -v, --verbose         verbose output
  --version             program version
```

### Basic Operation:
+ *default*: will try to match the input url(s) to a specific goblin. the matched goblin(s) will download what images they can according to their rule sets, in the highest possible quality. if no goblin is matched a generic goblin is used. if a text file is used as input, the path of the text file should be input using the ```--local``` argument.

	*examples:*

	```bash
	image-goblin --verbose https://www.website.com/pages/somewebpage.html

	image-goblin --local urls.txt --noskip

	echo https://www.website.com/pages/somewebpage.html | xargs image-goblin --dir temp/images --silent
	```

### Mode Specific Operation:
+ *generic goblin:* for any site without a specific goblin. by default, this goblin will automatically try to remove common cropping. using the ```--format``` option overrides this functionality and instead formats according to user input modifier(s). the usage format for this is ```--format "action modifier[ replacement]"```. ```"add modifier"``` will append the modifier to the end of the url; for example a query string. ```"sub modifier replacement"``` substitutes, while ```"rem modifier"``` removes. the modifier can be a regular string or regex pattern. the entire format argument needs to be quoted. using the ```--noup``` flag prevents any automatic manipulation of urls. you can also enforce greedy mode with ```--greedy```; sometimes this will find more images.

	*examples:*

	```bash
	image-goblin -f "rem -\d+x\d+" https://website.com/pages/somewebpage.html

	image-goblin --format "sub size=\w+ size=large" https://website.com/uploadsimage_01.jpg?size=some_size
	```

+ *iterator goblin:* when provided a url, this goblin will try to download that file and all other files with the same url structure that are on the server (but not necessarily displayed on the website). the iterable needs to be surrounded by '#' on either side when input to be assigned to the iterator goblin and also indicate the portion of the url to be iterated. use the ```--step``` argument to set step size (default 1); negative values will iterate down. set ```--timeout 0``` to prevent timing out after n failed attempts.

	*example:*

	```bash
	image-goblin --timeout 10 --delay 3 https://website.com/uploads/image_#01#.jpg
	```

	the program will then iterate that url:

	* https://website.com/uploads/image_01.jpg
	* https://website.com/uploads/image_02.jpg
	* https://website.com/uploads/image_03.jpg
	* https://website.com/uploads/image_04.jpg
	* https://website.com/uploads/image_05.jpg
	* ...
	* https://website.com/uploads/image_107.jpg

	etc...

+ *feed:* using the feed flag, you can accumulate urls by inputting them one by one. this is useful for accumulating urls as you find them while browsing the web, and downloading all at once. press "enter" with an empty input when finished. try it :)

+ *other goblins:* with a few exceptions (see ```--help``` for more info), all other goblins are self contained and require no explanation.

#### Misc:
+ a specific goblin can be forced using ```--goblin```.
+ a random delay (0<=n<=10) can be used with ```--delay -1```
+ the ```--format``` input needs to be exact so make sure modifiers/spaces have not been erroneously added or left out.
+ if little or no (relevant) images are found then the page is probably generated dynamically with javascript which the program does not handle. you can also try with the ```--noup``` and ```--greedy``` handles.
