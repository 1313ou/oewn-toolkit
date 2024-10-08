#!/usr/bin/python3

import argparse
import os
import pickle

import wordnet_toyaml


def save_pickle(wn, repo):
    pickle.dump(wn, open("%s/wn.pickle" % repo, "wb"))


def load_pickle(repo):
    return pickle.load(open("%s/wn.pickle" % repo, "rb"))


def load(repo):
    current_dir = os.getcwd()
    os.chdir(repo)
    wn = wordnet_yaml.load()
    os.chdir(current_dir)
    return wn


def save(wn, repo):
    current_dir = os.getcwd()
    os.chdir(repo)
    wordnet_yaml.save(wn)
    os.chdir(current_dir)
    return wn
