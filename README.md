pyvideo-urlgrabber
==================

This is a very basic script that parses the metadata on http://pyvideo.org for the source video URLs, and prints them to stdout.

Use it like this:

```bash
./pyvideo-urlgrabber.py --category "PyCon US 2014"

http://www.youtube.com/watch?v=GeQt7CxzmPo
http://www.youtube.com/watch?v=nAqklQ4wzhY
http://www.youtube.com/watch?v=SBQB_yS2K4M
http://www.youtube.com/watch?v=Kdrp1Kt1dSw
[...]
```

The idea is to then feed these URLs into other purpose-built tools.

The first run will take a while, as it builds a cache of all the JSON metadata available on the site. There are currently over 2000 videos, resulting in a cache of around 4MB. This data is saved to a local cache file that must be manually rebuilt (using the `-r` option) to pick up new changes.

In addition to being able to filter to a specific category, you can also filter by a speaker name or video file type.
