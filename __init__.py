# -*- coding: utf-8 -*-
# Name: Right Hand Answer Shortcuts
# Copyright: Julien Baley
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
# Adapted for Anki 2.1 from Vitalie Spinu's Anki 2.0 add-on
#
# Binds 'j', 'h', 'k', 'l' to answer buttons. This allows the right hand to
# rest on the middle line of the keyboard. The rationale behind the choice of
# shortcuts is the following: fail / normal are the most common buttons (j, k)
# hard is fairly rare (in my usage) so it can be a bit out of the way in 'h'
# and easy is simply to the right of normal, 'l'. The original's add-on jkl;
# wasn't to my taste. As a bonus 'z' is bound to undo.
#
# Additionally, you can answer normal/easy on a failed card and it will do the
# right thing. You can also answer a card while in question state (which is
# convenient if you review tons of cards and need speed).
# 

from aqt import mw
from aqt.reviewer import Reviewer
from anki.hooks import wrap

def shortcutKeys(self, _old):
    return [
            ("h", lambda: self._answerCard(1)),  # fail
            ("j", lambda: self._answerCard(2)),  # hard
            # to guarantee that 'k' is always normal, it needs to be the button
            # to the left of the rightmost one (i.e. 4-1 for review, 3-1 for
            # new/learning cards).
            ("k", lambda: self._answerCard(
                self.mw.col.sched.answerButtons(self.card) - 1)),  # normal
            ("l", lambda: self._answerCard(4)),  # easy
            ("z", lambda: mw.onUndo()),  # undo (a bit hacky but works for me)
        ] + _old(self)


def answerCard(self, ease, _old):
    if self.state == "question":
        self.state = 'answer'

    _old(self, min(self.mw.col.sched.answerButtons(self.card), ease))
    

Reviewer._shortcutKeys = wrap(Reviewer._shortcutKeys, shortcutKeys, "around")
Reviewer._answerCard = wrap(Reviewer._answerCard, answerCard, "around")

