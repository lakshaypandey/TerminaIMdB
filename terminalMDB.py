#!/usr/bin/python

import urllib
import argparse
import sys
from xml.etree import ElementTree


def retrieveMovie(title, is_ID):
    title = urllib.quote(title.encode("utf8"))
    if is_ID:
        URL = "http://www.omdbapi.com/?r=xml&plot=full&i=%s" % title
    else:
        URL = "http://www.omdbapi.com/?r=xml&plot=full&t=%s" % title
    xml = ElementTree.parse(urllib.urlopen(URL))
    # fall back to movie search if no movie is found
    for A in xml.iter('root'):
        if (A.get('response') == 'False'):
            print "Movie not found!"
            sys.exit()
    xml = xml.getroot()
    printInfo(xml)
    return xml

# Search for movie and return plot for all the results


def movieSearch(title):
    title = urllib.quote(title.encode("utf8"))
    URL = "http://www.omdbapi.com/?r=xml&s=%s" % title
    xml = ElementTree.parse(urllib.urlopen(URL))
    xml = xml.getroot()
    for B in xml.findall('Movie'):
        apicall = retrieveMovie(B.get('imdbID'), True)
    return xml


def printInfo(xml):
    for B in xml.findall('movie'):
        print "\n%s (%s) || %s || %s\n" % (B.get('title'), B.get('year'),
                                           B.get('runtime'),
                                           B.get('imdbRating'))
        print "Director: %s\nActors: %s\n" % (B.get('director'),
                                              B.get('actors'))
        print "%s\n" % (B.get('plot'))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Command-Line Interface for the IMdB')

    parser.add_argument("-t", help="Search by title. Return first result")
    parser.add_argument("-i", help="Search by id")
    parser.add_argument("-s", help="Search and return results")

    args = parser.parse_args()

    if args.t:
        retrieveMovie(args.t, False)
    elif args.i:
        retrieveMovie(args.i, True)
    elif args.s:
        movieSearch(args.s)
    else:
        parser.print_help()
