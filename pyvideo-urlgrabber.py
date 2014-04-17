#!/usr/bin/env python
#
# Simple script to print download URLs for PyCon videos.

import json
import optparse
import os
import sys
import urllib2


def get_videos():
    """Return a json array of all videos available on the site, built
    by fetching each page sequentially until there are no more pages."""
    videos = []
    page = 0
    end_of_pages = False
    while not end_of_pages:
        page += 1
        url = "http://pyvideo.org/api/v2/video?page=%s" % str(page)
        try:
            data = json.load(urllib2.urlopen(url))
        except urllib2.HTTPError as e:
            print "Got error %s, quitting early." % e
            break

        videos.extend(data["results"])
        if data["next"] == None:
            end_of_pages = True
    return json.dumps(videos)


def main():
    # Mapping of format option to video metadata keys
    video_formats = {
        "youtube": "source_url",
        "mp4": "video_mp4_url", 
        "ogv": "video_ogv_url",
        "webm": "video_webm_url",
        "flv": "video_flv_url",
        }

    o = optparse.OptionParser()
    o.description = \
        ("Print out a plain line-separated list of download URLs for videos on "
        "pyvideo.org, filterable by speaker, category and video format. "
        "On first run, the site's metadata "
        "is cached to a local JSON file. Because fetching the metadata is "
        "time-consuming and expensive, and content does not change daily, "
        "the cache must be manually rebuilt in order to pick up newer videos.")
    o.add_option("-c", "--category", default=None,
        help="Restrict results to a specific category, ie. 'PyCon US 2014'.")
    o.add_option("-s", "--speaker", default=None,
        help="Restrict results to a specific speaker.")
    o.add_option("-r", "--rebuild-cache", default=False, action="store_true",
        help="Rebuild the cache of videos before returning results.")
    o.add_option('-f', "--format", default=None,
        help="Restrict results to only the given format. Must be one of: "
             "%s. There's otherwise no 'preferred' format."
             % ", ".join(video_formats.keys()))
    opts, args = o.parse_args()

    if opts.format:
        if opts.format not in video_formats:
            o.print_help()
            sys.exit(1)
        valid_formats = [video_formats[opts.format]]
    else:
        valid_formats = video_formats.values()

    # Cache all the metadata if we need to
    json_cache = os.path.join(os.path.dirname(__file__), "pyvideo_cache.json")
    if not os.path.exists(json_cache) or opts.rebuild_cache:
        videos = get_videos()
        with open(json_cache, "w") as cache:
            cache.write(videos)

    with open(json_cache, "r") as cache:
        videos = json.load(cache)

    # Filter out results if we gave category, speaker, format options
    matching_videos = videos[:]

    if opts.category:
        matching_videos = [v for v in matching_videos if opts.category == v["category"]]
    if opts.speaker:
        matching_videos = [v for v in matching_videos if opts.speaker in v["speakers"]]
    if opts.format:
        matching_videos = [v for v in matching_videos if v.get(video_formats[opts.format])]

    urls = set()

    for v in matching_videos:
        # Filter URLs by format here if we've given a format
        for k in valid_formats:
            if v.get(k):
                urls.add(v[k])
                break

    for u in urls:
        print(u)


if __name__ == '__main__':
    main()
