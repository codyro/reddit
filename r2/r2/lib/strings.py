# The contents of this file are subject to the Common Public Attribution
# License Version 1.0. (the "License"); you may not use this file except in
# compliance with the License. You may obtain a copy of the License at
# http://code.reddit.com/LICENSE. The License is based on the Mozilla Public
# License Version 1.1, but Sections 14 and 15 have been added to cover use of
# software over a computer network and provide for limited attribution for the
# Original Developer. In addition, Exhibit A has been modified to be consistent
# with Exhibit B.
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License for
# the specific language governing rights and limitations under the License.
#
# The Original Code is Reddit.
#
# The Original Developer is the Initial Developer.  The Initial Developer of the
# Original Code is CondeNet, Inc.
#
# All portions of the code written by CondeNet are Copyright (c) 2006-2010
# CondeNet, Inc. All Rights Reserved.
################################################################################
"""
Module for maintaining long or commonly used translatable strings,
removing the need to pollute the code with lots of extra _ and
ungettext calls.  Also provides a capacity for generating a list of
random strings which can be different in each language, though the
hooks to the UI are the same.
"""

import helpers as h
from pylons import g
from pylons.i18n import _, ungettext
import random, locale

__all__ = ['StringHandler', 'strings', 'PluralManager', 'plurals',
           'Score', 'rand_strings']

# here's where all of the really long site strings (that need to be
# translated) live so as not to clutter up the rest of the code.  This
# dictionary is not used directly but rather is managed by the single
# StringHandler instance strings
string_dict = dict(

    banned_by = "removed by %s",
    banned    = "removed",
    reports   = "reports: %d",
    
    # this accomodates asian languages which don't use spaces
    number_label = _("%(num)d %(thing)s"),

    # this accomodates asian languages which don't use spaces
    points_label = _("%(num)d %(point)s"),

    # this accomodates asian languages which don't use spaces
    time_label = _("%(num)d %(time)s"),

    # this accomodates asian languages which don't use spaces
    float_label = _("%(num)5.3f %(thing)s"),

    # this is for Japanese which treats people counds differently
    person_label = _("<span class='number'>%(num)s</span>&#32;<span class='word'>%(persons)s</span>"),

    firsttext = _("reddit is a source for what's new and popular online. vote on links that you like or dislike and help decide what's popular, or submit your own!"),

    already_submitted = _("that link has already been submitted, but you can try to [submit it again](%s)."),

    multiple_submitted = _("that link has been submitted to multiple reddits. you can try to [submit it again](%s)."),

    user_deleted = _("your account has been deleted, but we won't judge you for it."),

    cover_msg      = _("you'll need to login or register to do that"),
    cover_disclaim = _("(don't worry, it only takes a few seconds)"),

    legal = _("I understand and agree that registration on or use of this site constitutes agreement to its %(user_agreement)s and %(privacy_policy)s."),
    
    friends = _('to view reddit with only submissions from your friends, use [reddit.com/r/friends](%s)'),

    sr_created = _('your reddit has been created'),

    active_trials = _("we haven't yet decided whether these things are spam, so you have a chance to change your vote:"),
    finished_trials = _("it's too late to change your vote on these things (the verdict has been issued):"),
    more_info_link = _("visit [%(link)s](%(link)s) for more information"),

    msg_add_friend = dict(
        friend = None,
        moderator = _("you have been added as a moderator to [%(title)s](%(url)s)."),
        contributor = _("you have been added as an approved submitter to [%(title)s](%(url)s)."),
        banned = _("you have been banned from posting to [%(title)s](%(url)s)."),
        traffic = _('you have been added to the list of users able to see [traffic for the sponsored link "%(title)s"](%(traffic_url)s).')
        ),

    subj_add_friend = dict(
        friend = None,
        moderator = _("you are a moderator"),
        contributor = _("you are an approved submitter"),
        banned = _("you've been banned"),
        traffic = _("you can view traffic on a promoted link")
        ),
    
    sr_messages = dict(
        empty =  _('you have not subscribed to any reddits.'),
        subscriber =  _('below are the reddits you have subscribed to'),
        contributor =  _('below are the reddits that you are an approved submitter on.'),
        moderator = _('below are the reddits that you have moderator access to.')
        ),
    
    sr_subscribe =  _('click the `+frontpage` or `-frontpage` buttons to choose which reddits appear on your front page.'),

    searching_a_reddit = _('you\'re searching within the [%(reddit_name)s](%(reddit_link)s) reddit. '+
                           'you can also search within [all reddits](%(all_reddits_link)s)'),

    css_validator_messages = dict(
        broken_url = _('"%(brokenurl)s" is not a valid URL'),
        invalid_property = _('"%(cssprop)s" is not a valid CSS property'),
        invalid_val_for_prop = _('"%(cssvalue)s" is not a valid value for CSS property "%(cssprop)s"'),
        too_big = _('too big. keep it under %(max_size)dkb'),
        syntax_error = _('syntax error: "%(syntaxerror)s"'),
        no_imports = _('@imports are not allowed'),
        invalid_property_list = _('invalid CSS property list "%(proplist)s"'),
        unknown_rule_type = _('unknown CSS rule type "%(ruletype)s"')
    ),
    submit_box_text = _('to anything interesting: news article, blog entry, video, picture...'),
    permalink_title = _("%(author)s comments on %(title)s"),
    link_info_title = _("%(title)s : %(site)s"),
    banned_subreddit = _("""**this reddit has been banned**\n\nmost likely this was done automatically by our spam filtering program. the program is still learning, and may even have some bugs, so if you feel the ban was a mistake, please send a message to [our site admins](%(link)s) and be sure to include the **exact name of the reddit**."""),
    comments_panel_text = _("""The following is a sample of what Reddit users had to say about this page. The full discussion is available [here](%(fd_link)s); you can also get there by clicking the link's title (in the middle of the toolbar, to the right of the comments button)."""),

    submit_link = _("""You are submitting a link. The key to a successful submission is interesting content and a descriptive title."""),
    submit_text = _("""You are submitting a text-based post. Speak your mind. A title is required, but expanding further in the text field is not. Beginning your title with "vote up if" is violation of intergalactic law."""),
    iphone_first = _("You should consider using [reddit's free iphone app](http://itunes.com/apps/iredditfree)."),
    verify_email = _("we're going to need to verify your email address for you to proceed."),
    verify_email_submit = _("you'll be able to submit more frequently once you verify your email address"),
    email_verified =  _("your email address has been verfied"),
    email_verify_failed = _("Verification failed.  Please try that again"),
    search_failed = _("Our search machines are under too much load to handle your request right now. :( Sorry for the inconvenience. [Try again](%(link)s) in a little bit -- but please don't mash reload; that only makes the problem worse."),
    generic_quota_msg = _("You've submitted too many links recently. Please try again in an hour."),
    verified_quota_msg = _("You've submitted several links recently that haven't been doing very well. You'll have to wait a while before you can submit again, or [write to the moderators of this reddit](%(link)s) and ask for an exemption."),
    unverified_quota_msg = _("You haven't [verified your email address](%(link1)s); until you do, your submitting privileges will be severely limited. Please try again in an hour or verify your email address. If you'd like an exemption from this rule, please [write to the moderators of this reddit](%(link2)s)."),
    read_only_msg = _("reddit is in \"emergency read-only mode\" right now. :( you won't be able to log in. we're sorry, and are working frantically to fix the problem."),
)

class StringHandler(object):
    """Class for managing long translatable strings.  Allows accessing
    of strings via both getitem and getattr.  In both cases, the
    string is passed through the gettext _ function before being
    returned."""
    def __init__(self, **sdict):
        self.string_dict = sdict

    def __getitem__(self, attr):
        try:
            return self.__getattr__(attr)
        except AttributeError:
            raise KeyError
    
    def __getattr__(self, attr):
        rval = self.string_dict[attr]
        if isinstance(rval, (str, unicode)):
            return _(rval)
        elif isinstance(rval, dict):
            return dict((k, _(v)) for k, v in rval.iteritems())
        else:
            raise AttributeError

strings = StringHandler(**string_dict)


def P_(x, y):
    """Convenience method for handling pluralizations.  This identity
    function has been added to the list of keyword functions for babel
    in setup.cfg so that the arguments are translated without having
    to resort to ungettext and _ trickery."""
    return (x, y)

class PluralManager(object):
    """String handler for dealing with pluralizable forms.  plurals
    are passed in in pairs (sing, pl) and can be accessed via
    self.sing and self.pl.

    Additionally, calling self.N_sing(n) (or self.N_pl(n)) (where
    'sing' and 'pl' are placeholders for a (sing, pl) pairing) is
    equivalent to ungettext(sing, pl, n)
    """
    def __init__(self, plurals):
        self.string_dict = {}
        for s, p in plurals:
            self.string_dict[s] = self.string_dict[p] = (s, p)

    def __getattr__(self, attr):
        if attr.startswith("N_"):
            a = attr[2:]
            rval = self.string_dict[a]
            return lambda x: ungettext(rval[0], rval[1], x)
        else:
            rval = self.string_dict[attr]
            n = 1 if attr == rval[0] else 5
            return ungettext(rval[0], rval[1], n)

plurals = PluralManager([P_("comment",     "comments"),
                         P_("point",       "points"),
                         
                         # things
                         P_("link",        "links"),
                         P_("comment",     "comments"),
                         P_("message",     "messages"),
                         P_("subreddit",   "subreddits"),
                         
                         # people
                         P_("reader",  "readers"),
                         P_("subscriber",  "subscribers"),
                         P_("approved submitter", "approved submitters"),
                         P_("moderator",   "moderators"),
                         
                         # time words
                         P_("milliseconds","milliseconds"),
                         P_("second",      "seconds"),
                         P_("minute",      "minutes"),
                         P_("hour",        "hours"),
                         P_("day",         "days"),
                         P_("month",       "months"),
                         P_("year",        "years"),
])


class Score(object):
    """Convienience class for populating '10 points' in a traslatible
    fasion, used primarily by the score() method in printable.html"""
    @staticmethod
    def number_only(x):
        return str(max(x, 0))

    @staticmethod
    def points(x):
        return  strings.points_label % dict(num=x, point=plurals.N_points(x))

    @staticmethod
    def safepoints(x):
        return  strings.points_label % dict(num=max(x,0), 
                                            point=plurals.N_points(x))

    @staticmethod
    def _people(x, label):
        return strings.person_label % \
            dict(num = locale.format("%d", x, True),
                 persons = label(x))

    @staticmethod
    def subscribers(x):
        return  Score._people(x, plurals.N_subscribers)

    @staticmethod
    def readers(x):
        return  Score._people(x, plurals.N_readers)

    @staticmethod
    def none(x):
        return ""


def fallback_trans(x):
    """For translating placeholder strings the user should never see
    in raw form, such as 'funny 500 message'.  If the string does not
    translate in the current language, falls back on the g.lang
    translation that we've hopefully already provided"""
    t = _(x)
    if t == x:
        l = h.get_lang()
        h.set_lang(g.lang, graceful_fail = True)
        t = _(x)
        if l and l[0] != g.lang:
            h.set_lang(l[0])
    return t

class RandomString(object):
    """class for generating a translatable random string that is one
    of n choices.  The 'description' field passed to the constructor
    is only used to generate labels for the translation interface.

    Unlike other translations, this class is accessed directly by the
    translator classes and side-step babel.extract_messages.
    Untranslated, the strings return are of the form 'description n+1'
    for the nth string.  The user-facing versions of these strings are
    therefore completely determined by their translations."""
    def __init__(self, description, num):
        self.desc = description
        self.num = num
    
    def get(self, quantity = 0):
        """Generates a list of 'quantity' random strings.  If quantity
        < self.num, the entries are guaranteed to be unique."""
        l = []
        possible = []
        for x in range(max(quantity, 1)):
            if not possible:
                possible = range(self.num)
            irand = random.choice(possible)
            possible.remove(irand)
            l.append(fallback_trans(self._trans_string(irand)))

        return l if len(l) > 1 else l[0]

    def _trans_string(self, n):
        """Provides the form of the string that is actually translated by gettext."""
        return "%s %d" % (self.desc, n+1)

    def __iter__(self):
        for i in xrange(self.num):
            yield self._trans_string(i)
                   

class RandomStringManager(object):
    """class for keeping randomized translatable strings organized.
    New strings are added via add, and accessible by either getattr or
    getitem using the short name passed to add."""
    def __init__(self):
        self.strings = {}

    def __getitem__(self, attr):
        return self.strings[attr].get()

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError

    def get(self, attr, quantity = 0):
        """Convenience method for getting a list of 'quantity' strings
        from the RandomString named 'attr'"""
        return self.strings[attr].get(quantity)

    def add(self, name, description, num):
        """create a new random string accessible by 'name' in the code
        and explained in the translation interface with 'description'."""
        self.strings[name] = RandomString(description, num)

    def __iter__(self):
        """iterator primarily used by r2.lib.translations to fetch the
        list of random strings and to iterate over their names to
        insert them into the resulting .po file for a given language"""
        return self.strings.iteritems()

rand_strings = RandomStringManager()

rand_strings.add('sadmessages',   "Funny 500 page message", 10)
rand_strings.add('create_reddit', "Reason to create a reddit", 20)
